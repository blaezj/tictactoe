import sys
import time
from backend import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


BUTTONSTYLE = """
    QPushButton {
        border: 1px;
        border-width: 2px;
        border-radius: 20px;
        background-color: rgb(0, 80, 157);
        }

    QPushButton:hover {
        background-color: rgb(255, 213, 0);
        padding: 20px;
        border-radius: 5px;

    }
"""

WINDOWSTYLE = """
    QWidget {
        background-color: rgb(0, 63, 136);
    
    }


"""


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread
    
    finished:
        no data, game over :) returns int of player who won
    
    error
        dont know when or how this would send

    inputNeeded
        we need input from whichever play is next!

    result
        return board data, allowing us to map 
        the new board

    '''

    finished = pyqtSignal(str)
    

class Worker(QRunnable):
    '''
    Worker thread

    fn is the function we pass to the worker to run
    '''
    def __init__(self, fn, game, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.game = game
        self.mutex = QMutex()
        self.wait_condition = QWaitCondition()
        self.pause = True

        # these are for the rows we recieve from
        # the user input
        # it was easier to just make it apart of the worker object 
        self.row = -1
        self.col = -1

        # args and kwargs
        self.args = args
        self.kwargs = kwargs

        # i dont use these signals really
        self.signals = WorkerSignals()

    
    '''
    Below is essentially the state machine which will run the
    back end.
    Wasn't sure how to keep this all seperate from the front end,
    so I just kept it in a worker thread which will forever
    loop and wait for input.

    '''
    @pyqtSlot()
    def run(self):
        # init the runner func with passed args kwargs
        print("thread start")
        #self.signals.inputNeeded.connect(self.inputReciever)

        self.fn(*self.args, **self.kwargs)
        while(True):

            # uses walrus op to assign result to checkWin, 
            # result is a tuple of (bool, str)
            if((result := self.game.checkWin())[0]):
                winner = result[1]
                self.signals.finished.emit(winner)
                break;

            
            # delete boxes that are too old
            self.game.deleteOldBoxes()
            
            # gui update
            self.fn(*self.args, **self.kwargs)

            # determine who is next!
            self.game.determineTurn()
            
            # this letter is the symbol for whoever is next
            let = self.game.gamePlayers_list[game.currentPlayerTurn].playerSymbol
            

                      
            # this pauses until we recieve and input from one of the buttons
            # aka, just wait for input.
            # this is unlocked within the function which recieves input
            self.mutex.lock()
            if self.pause:
                print("waiting...")
                self.wait_condition.wait(self.mutex)
            self.mutex.unlock()
           

            # might seem weird, but this way if the player picks
            # a spot already chosen, we just double rotate back to them
            if(not self.game.completeTurn(self.row, self.col, let)):
                self.game.rotateTurn()
                self.game.removeOneFromTime()

            self.pause = True
            
            # gui update 
            self.fn(*self.args, **self.kwargs)
            
            #self.game.board.printBoard()
            # rotates to next persons turn
            self.game.rotateTurn()
    

        print("thread done")

    def unpause(self):
        self.mutex.lock()
        self.pause = False
        self.mutex.unlock()
        self.wait_condition.wakeOne()
    
    def inputReciever(self, location):
        print("at row/co" location[:2])
        self.row = location[1]
        self.col = location[0]
        self.unpause()
                

# Subclass of QMainWindow
class Window(QWidget):
    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # the backedn game! we need to pass this to the worker thread
        # the worker thread RUNS the game
        self.game = game

        # lowkey dont know what this do
        self.threadpool = QThreadPool()
        print("Multithreading with max %d threads" % self.threadpool.maxThreadCount())
       
        # below creates worker thread to run backedn
        self.worker = Worker(self.guiUpdate, self.game)
        self.setWindowTitle("Super TicTacToe")
        
        # create instance
        self.layout = QGridLayout()

        # below creates buttons and connects button to func
        self.arrButtons = [None] * 9
        for i in range(9):
            self.arrButtons[i] = QPushButton("_")
            self.arrButtons[i].pressed.connect(self.buttonClicked)
            self.arrButtons[i].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.arrButtons[i].setStyleSheet(BUTTONSTYLE)

        # adds all widgets to grid
        buttonNum = 0
        for i in range(3):
            for j in range(3):
                self.layout.addWidget(self.arrButtons[buttonNum], i, j)
                buttonNum += 1
        
        self.xicon = QIcon('x.png')
        
        self.oicon = QIcon('o.png')
        #button2.setIcon(QtGui.QIcon('x.png'))
        #button2.setIconSize(QtCore.QSize(100,100))
 
        #button3.setIcon(QtGui.QIcon('x.png'))
        #button3.setIconSize(QtCore.QSize(100,100))

        self.setLayout(self.layout)
        self.setStyleSheet(WINDOWSTYLE)
        self.threadpool.start(self.worker)
              
    '''
    This function executes on a button click.
    It gets the index of the button
    and updates it subsequently on the backend with
    the inputReciever function
    '''
    def buttonClicked(self):
        button = self.sender()
        index = self.layout.indexOf(button)
        location = self.layout.getItemPosition(index)
        self.worker.inputReciever(location)
        
        #print("button", button, "at row/col", location[:2])

    '''
    updates the gui by going through the entire
    arr and updating based on what it finds
    '''
    def guiUpdate(self):
        index = 0
        rowNum = 0
        for row in self.game.board.arr:
            colNum = 0
            for col in row:
                # gross piece of code below
                # this just sets the text of the button
                # to the letter corresponding on the backend
                # representation of the array
                
                icon = self.game.board.checkFilledBy(rowNum, colNum)

                # self.arrButtons[index].setText(self.game.board.checkFilledBy(rowNum, colNum))
                

                # the code below should be changed if we want code
                # which can have more than 2 players
                if(icon == 'x'):
                    self.arrButtons[index].setIcon(self.xicon)
                
                if(icon == 'o'):
                    self.arrButtons[index].setIcon(self.oicon)

                if(icon == '_'):
                    self.arrButtons[index].setIcon(QIcon())

                # increment these two
                index += 1
                colNum += 1

            rowNum += 1

# create core components of the game
board = TicTacToeBoard()
players = [Player(), Player()]
game = Game(players, board)

# front end component
app = QApplication(sys.argv)
window = Window(game)
window.show()

app.exec()

