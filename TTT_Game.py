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
        # if move_count gets to 9 without a winner the game is a draw
        self.move_count = 0
        # set the marker for the player and computer accordingly
        if self.player_first:
            self.player_marker = "X"
            self.comp_marker = "O"
        else:
            self.player_marker = "O"
            self.comp_marker = "X"
        
    # when invoked AI_move claims the first available space for the computer
    # returns True to indicate game over
    # return False to indicate continue game	
    def AI_move(self):
        for row in range(len(self.board)): 
            for col in range(len(self.board[row])):
                if self.board[row][col] == " ":
                    return self.place_move(self.comp_marker, (row, col))
    # when invoked player_move claims the space indicated by coordinates
    # returns True to indicate game over
    # returns False to indicate continue game
    def player_move(self, coordinates):
        return self.place_move(self.player_marker, coordinates)
            
    # when invoked place_move changes the board to the indicated marker at the indicated coordinates
    # return True to indicate game over
    # return False to indicate continue game
    def place_move(self, marker, coordinates):
        self.board[coordinates[0]][coordinates[1]] = marker
        return self.check_board(coordinates)

    # when invoked print_board prints the information stored in board as a formated tic tac toe board
    def print_board(self):
        '''
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
        '''
        print(self.board_to_str(), end='')

    # when invoked board_to_str converts the board into a string and returns the string object
    def board_to_str(self):
        ret_str = ""
        count = 0;
        for line in self.board:
            for pos in range(len(line)):
                ret_str += line[pos]
                if pos == 2:
                    ret_str += "\n"
                else:
                    ret_str += "|"
            if count < 2:
                ret_str += "_|_|_\n"
            else:
                ret_str += " | | \n"
            count += 1
        return ret_str

    # when invoked check_coords checks to see if the coordinates are valid for the board
    # returns True if the coordinates are valid
    # returns False if the coordinates are not valid
    def check_coords(self, coordinates):
        return self.board[coordinates[0]][coordinates[1]] == " "

    # when invoked check_board checks the board to see if there is a winner or stalemate
    # checks possible states based on the most recent move
    # if there is a winner an appropriate message is printed
    # return 1 if there is a winner 
    # return -1 if there is a stalemate
    # return 0 if there is not a winner
    def check_board(self, coordinates):
        # increment the move count
        self.move_count += 1
        # flag to indicate win condition
        win_flag = 0
        # check the row of the most recent move
        prev_pos = self.board[coordinates[0]][0]
        for i in range(len(self.board[coordinates[0]])-1):
            curr_pos = self.board[coordinates[0]][i+1]
            if curr_pos != prev_pos:
                win_flag = 0    
                break
            else:
                win_flag = 1
                prev_pos = curr_pos
        # check to see if the entire row matched
        if win_flag:
            # there was a winner
            self.print_winner(curr_pos)
            return 1

        # the row did not have a winner check the column   
        prev_pos = self.board[0][coordinates[1]]
        for i in range(len(self.board[coordinates[1]])-1):
            curr_pos = self.board[i+1][coordinates[1]]
            if curr_pos != prev_pos:
                win_flag = 0
                break
            else:
                win_flag = 1
                prev_pos = curr_pos
        # check to seee if the entire column matched
        if win_flag:
            # there was a winner
            self.print_winner(curr_pos)
            return 1
        # the column did not have a winner check to see if the coordinates match a diagonal
        if coordinates == (0,0) or coordinates == (1,1) or coordinates == (2,2):
            # check to seee if the entire diagonal matched
            if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2]:
                # there was a winner
                self.print_winner(curr_pos)
                return 1
        elif coordinates == (2,0) or coordinates == (1,1) or coordinates == (0,2):
            # check to seee if the entire diagonal matched
            if self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2]:
                # there was a winner
                self.print_winner(curr_pos)
                return 1 
        # there was not a winner check for a draw
        for row in self.board:
            for col in row:
                if col == " ":
                    # there is still a blank space 
                    return 0
        # a blank space was not found there was a draw
        print("Stalemate! It could have been worse!")
        return -1
            
    
    def print_winner(self, marker):
        # check to see if the winning marker belongs to the computer or player
        if self.player_marker == marker:
            # the player won
            print("Congrats! You won!")
        else:
            # the computer won
            print("You lost! Better luck next time!")
'''
# main to test the class
def main():
    print("Lets play Tic Tac Toe!")
    input_flag = 1
    while (input_flag):
        player_first = input("Would you like to go first? Y/n: ")
        if isinstance(player_first, str):
            player_first.upper()
            if player_first == "Y" or player_first == "N":
                input_flag = 0
            else:
                print("Please make a valid selection!")
        else:
            print("Please make a valid selection!")
    if player_first == "Y":
        game = Game(1)
        moves = 0
    else:
        game = Game()
        game.AI_move()
        moves = 1
    game_flag = 1
    while(game_flag):
        game.print_board()
        input_flag = 1
        while (input_flag):
            coor_raw = input("Enter the coordinates for your move seperated by a space (e.g. \"0 2\"): ")
            try:
                coordinates_raw = coor_raw.split()
                coordinates = (int(coordinates_raw[0]), int(coordinates_raw[1]))
                if coordinates[0] >= 0 and coordinates[0] <= 2 and coordinates[1] >= 0 and coordinates[1] <= 2:
                    input_flag = 0
                else:
                    # invalid input
                    print("Please enter valid coordinates between 0 and 2!")
            except TypeError: 
                print("TypeError: Please enter valid coordinates between 0 and 2!")
        if game.player_move(coordinates):
            game_flag = 0
        moves += 1
        if moves == 9:
            break
        if game.AI_move():
            game_flag = 0
        moves += 1
        if moves == 9:
            game_flag = 0
    game.print_board()
main() 
'''
