# the following code is from "Computer Networking a Top-Down Approach"
# by Kurose and Ross
# this code will be modified for the project's functionality
'''
from socket import *
serverName = '10.0.2.15'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowecase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
'''
from socket import *
import argparse
import signal
import sys

server_port = 12000
client_socket = socket(AF_INET, SOCK_DGRAM)


parser = argparse.ArgumentParser(description='Play Tic Tac Toe with a remote server!')
parser.add_argument('-c', help='indicates the client will go first', action='store_true')
parser.add_argument('-s', dest='server_name', help='specifies the IP of the server, this is required', required=True)
args = parser.parse_args()


game_flag = 1

init_user_str = 'INIT,1'
init_server_str = 'INIT,0'
move_str = 'MOVE'
disconnect_str = 'DCNT'

if args.c:
    # the user wants to go first
    message = init_user_str
else:
    # the server will go first
    message = init_server_str

def signal_handler(signal, frame):
    print('You pressed Ctrl+C')
    message = disconnect_str
    client_socket.sendto(message.encode(), (args.server_name, server_port)) 
    client_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

# send the message to initilize the game
client_socket.sendto(message.encode(), (args.server_name, server_port))

error_flag = 0
while game_flag:
    prev_msg = message
    response, server_address = client_socket.recvfrom(2048)
    # decode the response
    dec_rsp = response.decode().split(',')
    # check the response type
    if dec_rsp[0] == 'CRDR' or dec_rsp[0] == 'INVC':
        # the response indicates the server wants coordinates from the user
        # print the current board 
        print(dec_rsp[2])
        # get the coordinates using the prompt string provided by the server
        input_flag = 1
        while input_flag:
            coor_str_raw = input(dec_rsp[1])
            coordinates = coor_str_raw.split()
            if len(coordinates) < 2:
                print("Please use a space!")
            elif coordinates[0].isdigit and coordinates[1].isdigit():
                # both coordinates are numbers
                # check to see if the numbers fall into the correct range
                if int(coordinates[0]) >= 0 and int(coordinates[0]) < 3 and int(coordinates[1]) >= 0 and int(coordinates[1]) < 3:
                    # the coordinates are valid for the range of the board
                    # send the coordinates in the next message
                        message = move_str + ',' + coor_str_raw
                        input_flag = 0
            # check to see if the input was not valid
            if input_flag:
                print("Please enter valid coordinates!")
    elif dec_rsp[0] == 'EOG':
        # the game is over
        # print the current board
        print(dec_rsp[2])
        # print the end of game message
        print(dec_rsp[1])
        # send a disconnect message
        message = disconnect_str
     
    elif dec_rsp[0] == 'DCNT':
        # the server is disconecting
        # print the server's disconnect message
        print(dec_rsp[1])
        game_flag = 0
        ''' debug print '''
        # print('disconnect')
    
    elif dec_rsp[0] == 'ERR':
        # the server did not recieve the message correctly 
        # check to see if there is already an active error message
        if error_flag:
            # the previous message also failed exit the program
            print("Error sending message to server!")
            message = disconnect_str
            game_flag = 0
            error_flag = 2
        else:
            # this is the first error
            # attempt to resend the previous message
            message = prev_msg
            error_flag = 1
    # check to see if the server did not disconnect
    if not dec_rsp[0] == 'DCNT':
        # send the message
        client_socket.sendto(message.encode(), (args.server_name, server_port))
print('Thank you for playing!')
client_socket.close()
