import numpy as np

SYMBOLS = ["x", "o", "v"]


class Box:
    def __init__(self):
        self.filled: bool = False
        self.timeFilled: int = 0
        self.filledBy: str = '_'

class TicTacToeBoard:
    
    # definitely is a better way to do this
    # will figure that out later

    topleft = Box()
    topmiddle = Box()
    topright = Box()
    
    centerleft = Box()
    centermiddle = Box() 
    centerright = Box()

    bottomleft = Box()
    bottommiddle = Box()
    bottomright = Box()

    arr = np.array([[topleft, topmiddle, topright],
                   [centerleft, centermiddle, centerright],
                   [bottomleft, bottommiddle, bottomright]])
    
    def checkFilled(self, row: int, col: int) -> bool:
        return self.arr[row, col].filled

    def checkTimeFilled(self, row: int, col: int) -> int:
        return self.arr[row, col].timeFilled

    def checkFilledBy(self, col:int, row:int) -> str:
        return self.arr[row, col].filledBy

    def fillBox(self, row: int, col: int, fillWith: str) -> bool:
        
        # check if already filled
        if(self.checkFilled(row, col)):
            return False
        # else fill the spot
        self.arr[row, col].filled = True
        self.arr[row, col].filledBy = fillWith
        return True

    def unfillBox(self, row: int, col: int):
        self.arr[row, col].filled = False
        self.arr[row, col].filledBy = "_"
        self.arr[row, col].timeFilled = 0

    def clearBoard(self):
        rowNum = 0
        for row in self.arr:
            colNum = 0
            for col in row:
                self.unfillBox(rowNum, colNum)
                colNum += 1
            rowNum += 1

    def timeCheckBoard(self):
        rowNum = 0
        for row in self.arr:
            colNum = 0
            for col in row:
                if(self.checkFilled(rowNum, colNum)):
                    self.arr[rowNum, colNum].timeFilled += 1

                if(self.checkTimeFilled(rowNum, colNum) == 8):
                    # if we reached time unfill a box
                    #print("row: " + str(rowNum) + "col: " + str(colNum))
                    self.unfillBox(rowNum, colNum)
                   
                colNum += 1
            rowNum += 1

    # this removes one from the time btw
    def unTimeCheckBoard(self):
        rowNum = 0
        for row in self.arr:
            colNum = 0
            for col in row:
                if(self.checkFilled(rowNum, colNum)):
                    self.arr[rowNum, colNum].timeFilled -= 1
                colNum += 1
            rowNum += 1

    def checkRows(self) -> str:
        rowNum = 0
        for row in self.arr:
            # if that row has a filled row
            # note for anyone working on this:
            # to make this more modular, find a way
            # around hard coding these column values
            if(self.checkFilled(rowNum, 0)):
                areEqual = (self.arr[rowNum, 0].filledBy ==
                            self.arr[rowNum, 1].filledBy ==
                            self.arr[rowNum, 2].filledBy)

                # gross nested if statement dont @ me 
                if areEqual:
                    return self.arr[rowNum, 0].filledBy

            # increment for good luck <3 (and so we go to next row
            rowNum += 1               
        return "_"

    def checkColumns(self) -> str:
        colNum = 0
        for col in self.arr:
            # note for anyone working on this:
            # to make this more modular, find a way
            # around hard coding these row values
            if(self.checkFilled(0, colNum)):
                areEqual = (self.arr[0, colNum].filledBy ==
                            self.arr[1, colNum].filledBy ==
                            self.arr[2, colNum].filledBy)

                # gross nested if statement dont @ me 
                if areEqual:
                    return self.arr[0, colNum].filledBy

            # increment for good luck <3 (and so we go to next col
            colNum += 1               
        return "_"


    def checkDiagonals(self) -> str:
        # first check from top left to bottom right
        if(self.checkFilled(0, 0)):
            leftToRightEqual = (self.arr[0, 0].filledBy ==
                            self.arr[1, 1].filledBy ==
                            self.arr[2, 2].filledBy)
            if(leftToRightEqual):
                return self.arr[0,0].filledBy

        # genuinely need a better way to check this <3
        if(self.checkFilled(0, 2)):
            rightToLeftEqual = (self.arr[0, 2].filledBy ==
                            self.arr[1, 1].filledBy ==
                            self.arr[2, 0].filledBy)
            if(rightToLeftEqual):
                return self.arr[0,2].filledBy

        # return the shit
        return "_"

    def checkWin(self) -> (bool, str):
        print("checking win")

        rowWinner = self.checkRows()       
        if(rowWinner != "_"):
            print("winner is: " + rowWinner)
            return (True, rowWinner)

        colWinner = self.checkColumns()
        if(colWinner != "_"):
            print("winner is: " + colWinner)
            return (True, colWinner)

        diagWinner = self.checkDiagonals()
        if(diagWinner != "_"):
            print("winner is: " + diagWinner)
            return (True, diagWinner)

        return (False, "_")
        # implrement later
    
    def printBoard(self):
        rowNum = 0
        for row in self.arr:
            colNum = 0
            print("")
            for col in row:
                print(self.arr[rowNum, colNum].filledBy, end="")
                colNum += 1
            rowNum += 1


class Player:
    def __init__(self):
        playerNum: int = -1
        playerTurn: bool = False
        playerSymbol: str = None

    def chooseSymbol(self) -> str:
        return SYMBOLS[self.playerNum] 

class Game:
    gamePlayers_list: list[Player] = []
    winner: str = None
    # for easy keeping track of whso turn it is
    currentPlayerTurn: int = -1
    board: TicTacToeBoard = None

    def __init__(self, players_list: list[Player], board: TicTacToeBoard ):
        self.gamePlayers_list = players_list
        self.board = board
        self.winner = None

        # rotates through players given and assigns them a number
        for i in range(len(self.gamePlayers_list)):
            self.gamePlayers_list[i].playerNum = i
            # this chooses their symbol
            self.gamePlayers_list[i].playerSymbol = self.gamePlayers_list[i].chooseSymbol()
            
        # sets the first player to true
        if(len(self.gamePlayers_list) > 1):
            self.gamePlayers_list[0].playerTurn = True

    '''
    Resets the board sets winner to none and 
    gives first turn to whoever is next

    '''
    def resetGame(self):
        self.board.clearBoard()
        self.winner = None
        # sets the first player to true
        if(len(self.gamePlayers_list) > 1):
            self.gamePlayers_list[0].playerTurn = True
    
    # rotates to the next players
    def rotateTurn(self):
        for i in range(len(self.gamePlayers_list)):
            if(self.gamePlayers_list[i].playerTurn):
                # stop current player turn
                self.gamePlayers_list[i].playerTurn = False

                # put next player in first
                self.gamePlayers_list[(i + 1) % len(self.gamePlayers_list)].playerTurn = True
                
                return

    # goes through list to find which player is next
    def determineTurn(self) -> int: 
        for player in self.gamePlayers_list:
            if(player.playerTurn):
                self.currentPlayerTurn = player.playerNum
                return player.playerNum

    # given col and row will fill in that box in the board arr
    def completeTurn(self, row:int, col:int, let:str) -> bool:
        # returns true if succesful. else just call it again
        if(self.board.fillBox(row, col, let)):
            return True

        print("spot filled try again loser")
        return False

    # wrapper function
    def checkWin(self) -> (bool, str):
        win, winner = self.board.checkWin()
        self.winner = winner
        return (win, winner)
    
    # sort of wrapper
    def deleteOldBoxes(self):
        self.board.timeCheckBoard()
        return

    def removeOneFromTime(self):
        self.board.unTimeCheckBoard()
        return
