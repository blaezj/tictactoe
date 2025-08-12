from backend import TicTacToeBoard, Box, Player, Game
#import frontend

# key parts of game
board = TicTacToeBoard()
players = [Player(), Player()]
game = Game(players, board)

while(True):
    
    # check if win
    if(game.checkWin()):
        break;
    
    # this will kill any boxes > 7 seconds ensuring the game
    # doesnt end
    game.deleteOldBoxes()

    # this determins who is going next
    game.determineTurn() 
   

    # Below is the only section we need to add to the gui.
    # -------------------------------------------------#
    print("Player " + str(game.currentPlayerTurn)) 
    print("Please input row.")
    row = input("Row:")
    
    print("Please input column.")
    col = input("Column:")
    # -------------------------------------------------#


    let = game.gamePlayers_list[game.currentPlayerTurn].playerSymbol
       

    # need a way to loop this until the user inputs a valid number
    game.completeTurn(int(row), int(col), let)

    board.printBoard()
    
    game.rotateTurn()




