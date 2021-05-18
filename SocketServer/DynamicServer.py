from socket import *
from select import *
import pybithumb
import time
HOST = ''
PORT = 10000
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 생성
serverSocket = socket(AF_INET, SOCK_STREAM)

# 소켓 주소 정보 할당 
serverSocket.bind(ADDR)
print('bind')

# 연결 수신 대기 상태
serverSocket.listen(100)
print('listen')

# 연결 수락
clientSocekt, addr_info = serverSocket.accept()
print('accept')
print('—client information—')
print(clientSocekt)

copy = 0
# 클라이언트로부터 메시지를 가져옴
while True:
    price = pybithumb.get_current_price("BTC")
    time.sleep(0.5)
    price = clientSocekt.send(str(price).encode())

# 소켓 종료 
clientSocekt.close()
serverSocket.close()
print('close')