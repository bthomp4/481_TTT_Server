# Game class for the tic tac toe game
class Game(object):
    # when  constructing a Game object there is an optional paramter for player_first
    # if player_first is 1, the player makes the first move, the player is "X"
    # if player_first is 0 (default), the computer makes the first move, the computer is "X"
    def __init__(self, player_first = 0):
        # the board 2-d list holds the game board
        self.board = [[" ", " ", " "],[" ", " ", " "],[" ", " ", " "]]
        # indicates if the marker to be used by the player and computer
        self.player_first = player_first
        # set the marker for the player and computer accordingly
        if self.player_first:
            self.player_marker = "X"
            self.comp_marker = "O"
        else:
            self.player_marker = "O"
            self.comp_marker = "X"
        
    # when invoked AI_move claims the first available space for the computer
    # returns True to indicate a move was placed succesfully
    # return False to indicate a move was not placed succesfully	
    def AI_move(self):
        for row in range(len(self.board)): 
            for col in range(len(self.board[row])):
                if self.board[row][col] == " ":
                    self.place_move(self.comp_marker, (row, col))
                    return True
        return False

    # when invoked player_move claims the indicated coordinates for the player
    # returns True to indicate the move was valid
    # returns False to indicate the move was invalid
    def player_move(self, coordinates):
        if self.board[coordinate[0]][coordinates[1]] == " ":
            return self.place_move(self.placer_marker, coordinates)
        else:
            return False

    # when invoked place_move changes the board to the indicated marker at the indicated coordinates
    # return True to indicate the move was sucessfully placed
    # return False to indicate the move was not placed
    def place_move(self, marker, coordinates):
        self.board[coordinates[0]][coordinates[1]] = marker
        if self.board[coordinates[0][coordinates[1] == marker:
            return True
        else:
            return False

    # when invoked print_board prints the information stored in board as a formated tic tac toe board
    def print_board(self):
        count = 0;
        for line in self.board:
            for pos in range(len(line)):
                print(line[pos], end='')
                if pos == 2:
                    print()
                else:
                    print("|", end='')
            if count < 2:
                print("_|_|_")
            else:
                print(" | |")
            count += 1

    # when invoked check_board checks the board to see if there is a winner or stalemate
    # if there is a winner an appropriate message is printed
    # return True if there is a winner or stalemate
    # return False if there is not a winner
    def check_board(self):
        for line in self.board:
            for pos in range(len(line)):

# main to test the class
def main():
    print("In main")
    game = Game()
    game.print_board()
    game.place_move("O", (0,0))
    game.print_board()
    game.AI_move()
    game.print_board()
main()
