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
from TTT_Game import Game

import signal
import sys

server_port = 12000
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))


client_dict = dict()
get_coor_str = 'CRDR,Please enter the coordinates for your move sperated by a space (e.g. \"0 2\"): '
print('The server is ready to recieve')
invalid_coor_str = 'INVC,Those coordinates are invalid!\nPlease enter valid coordinates: '
discnt_client_str = 'DCNT,See you again soon!'
discnt_server_str = 'DCNT,Server Disconnected!'
win_str = 'EOG,Congrats! You won!'
loss_str = 'EOG,Sorry you lost! Better luck next time!'
stale_str = 'EOG,Stalemate! Try harder next time!'
err_str = 'ERR,Error message not recieved correctly!'

def signal_handler(signal, frame):
    print('You pressed Ctrl+C')
    # send a disconnect message to all clients
    for key in client_dict: 
        response = discnt_server_str
        server_socket.sendto(response.encode(), key)
    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while True:
    message, current_address = server_socket.recvfrom(2048)
    # decode the message
    dec_msg = message.decode().split(',')
    ''' debug print message id'''
    print(dec_msg[0])
   
    # check the message type
    if dec_msg[0] == 'INIT':
        # the message corresponds to a new connect
        # check to see if the current address corresponds to an entry in the client_dict
        if current_address not in client_dict:
            # the current address does not currently correspond to an active board
            # check to see if the player wants to start
            if dec_msg[1] == '1':
                # the player wants to start
                game = Game(1)
            else:
                # the computer starts
                game = Game()
                # have the computer make the first move
                game.AI_move()
            client_dict[current_address] = game
            response = get_coor_str
        else:
            print('client already exits')
        print(client_dict.items())
    elif dec_msg[0] == 'MOVE':
        # the message corresponds to a player move
        # check to see if the move is valid
        coor_raw = dec_msg[1].split()
        coordinates = (int(coor_raw[0]), int(coor_raw[1]))
        if client_dict[current_address].check_coords(coordinates):
            # the coordinates are valid place the move on the board
            game_over = client_dict[current_address].player_move(coordinates)
            # check to see if the game is over
            if game_over:
                # the game is over check to see if win or stalemate
                if game_over > 0:
                    # the client won
                    response = win_str
                else:
                    # there was a stalemate
                    response = stale_str
            else:
                # the game is not over yet have the AI make a move
                game_over = client_dict[current_address].AI_move()
                if game_over:
                    # the game is over check to see if win or stalemate
                    if game_over > 0:
                        # the server won
                        response = loss_str
                    else:
                        # there was a stalemate
                        response = stale_str
                else:
                    # the game is not over prompt for a new coordinate
                    response = get_coor_str
        else:
            # the coordinates are not valid 
            response = invalid_coor_str
    elif dec_msg[0] == 'DCNT':
        # The client is discontinuing the game
        # remove the client from the client_dict
        client_dict.pop(current_address)
        response = discnt_client_str
    else:
        # the message does not take the correct form
        response = err_str
    
    # the response has been calculated 
    # check to see if the client is still connected
    if not dec_msg[0] == 'DCNT':
        # append the game board to the message
        response = response + ',' + client_dict[current_address].board_to_str()
    # send the response back to the client
    server_socket.sendto(response.encode(), current_address)
