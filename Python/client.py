from socket import *
from select import *
import sys
from time import ctime

HOST = '127.0.0.1'
PORT = 10001
BUFSIZE = 1024
ADDR = (HOST,PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)# 서버에 접속하기 위한 소켓을 생성한다.

clientSocket.connect(ADDR)# 서버에 접속을 시도한다.

print('connect is success')

while True:
    data = clientSocket.recv(65535)	# 서버에 메시지 전달
    print('btc : ', data.decode())