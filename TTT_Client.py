# the following code is from "Computer Networking a Top-Down Approach"
# by Kurose and Ross
# this code will be modified for the project's functionality

from socket import *
serverName = '10.0.2.15'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input lowecase sentence:')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()

