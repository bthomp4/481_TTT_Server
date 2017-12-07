# the following code is from "Computer Networking a Top-Down Approach"
# by Kurose and Ross
# this code will be modified for the project's funstionality
'''
from socket import *
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('',serverPort))
print("The server is ready to recieve")
while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
'''

from socket import *
import TTT_Game
server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((''.server_port))
client_dict = dict()
get_coor_str = "CRDR,Here is the current board:\n" + client_dict[current_address].board_to_str() + "\nPlease enter the coordinates for your move sperated by a space (e.g. \"0 2\"): "
print("The server is ready to recieve")
invalid_coor_str = "INVC,Those coordinates are invalid!\nPlease enter valid coordinates: "
discnt_client_str = "DCNT,See you again soon!"
discnt_server_str ="DCNT,Server Disconnected!"
win_str = "EOG,Congrats! You won!"
loss_str = "EOG,Sorry you lost! Better luck next time!"
stale_str = "EOG,Stalemate! Try harder next time!"
while True:
    message, current_address = server_socket.recvfrom(2048)
    # decode the message
    dec_msg = message.decode().split(";")
    # check the message type
    if dec_msg[0] == "INIT":
        # the message corresponds to a new connect
        # check to see if the current address corresponds to an entry in the client_dict
        if current_address not in client_dict:
            # the current address does not currently correspond to an active board
            # check to see if the player wants to start
            if dec_msg[1] == "1":
                # the player wants to start
                game = Game(1)
            else:
                # the computer starts
                game = Game()
                # have the computer make the first move
                game.AI_move()
            client_dict[current_address] = game
            response = get_coor_str
    elif dec_msg[0] == "MOVE":
        # the message corresponds to a player move
        # check to see if the move is valid
        coor_raw = dec_msg[1].split()
        coordinates = (int(coor_raw[0]), int(coor_raw[1]))
        if check_coords(coordinates):
            # the coordinates are valid place the move on the board
            game_over = client_dict[current_address].place_move(coordinates)
            # check to see if the game is over
            if game_over:
                # the game is over check to see if win or stalemate
                if game_over > 0:
                    # the client won

                
                 
        else:
            # the coordinates are not valid 
            response = invalid_coor_str
    elif dec_msg[0] == "DCNT":
        # The client is discontinuing the game
        # remove the client from the client_dict
        client_dict.pop(current_Address)
        response = discnt_str
