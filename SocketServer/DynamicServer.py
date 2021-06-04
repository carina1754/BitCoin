   # 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket, threading
import pyupbit
import time
import csv
access = "MguYI9AWXDf3BtegTqbz6Y2aCNsdMtFxSs34obL5" 
secret = "4jYkOYO70TCvhmDtCCOcejxAO3oIH5XdNLCZ2jg8" 

upbit = pyupbit.Upbit(access, secret) 

def printer():
    krw = upbit.get_balance("KRW")
    btc = upbit.get_balance("KRW-BTC")
    day = pyupbit.get_ohlcv("KRW-BTC", count=5)
    min5 = pyupbit.get_ohlcv("KRW-BTC", interval="minutes5", count=1)
    min30 = pyupbit.get_ohlcv("KRW-BTC", interval="minutes30", count=10)
    min3 = pyupbit.get_ohlcv("KRW-BTC", interval="minutes3", count=20)

    fp = open('data.csv', 'w', encoding='utf-8', newline='')
    wr = csv.writer(fp)

    for i in range(len(day.index)):
        wr.writerow(day.iloc[i])

    for i in range(len(min5.index)):
        wr.writerow(min5.iloc[i])

    for i in range(len(min30.index)):
        wr.writerow(min30.iloc[i])

    for i in range(len(min3.index)):
        wr.writerow(min3.iloc[i])

    fp.close()
# binder함수는 서버에서 accept가 되면 생성되는 socket 인스턴스를 통해 client로 부터 데이터를 받으면 echo형태로 재송신하는 메소드이다.
def binder(client_socket, addr):
    printer()
# 커넥션이 되면 접속 주소가 나온다.
    print('Connected by', addr);
    try:
        data_transferred = 0
    # 접속 상태에서는 클라이언트로 부터 받을 데이터를 무한 대기한다.
    # 만약 접속이 끊기게 된다면 except가 발생해서 접속이 끊기게 된다.
        while True:
            # price = pybithumb.get_current_price("BTC")
            time.sleep(0.5)
            data = client_socket.recv(1024)
            if data == 1 :
                krw = upbit.get_balance("KRW")
                btc = upbit.get_balance("KRW-BTC")
                upbit.buy_market_order("KRW-BTC", krw/10, contain_req=False)

            elif data == 2 :
                upbit.sell_market_order("KRW-BTC", btc, contain_req=False)

            # price = client_socket.send(str(price).encode())
            printer()
            print(1)
            with open("data.csv", 'rb') as f:
                data = f.read(4096) #1024바이트 읽는다
                while data: #데이터가 없을 때까지
                    print(data)
                    data_transferred += client_socket.send(data) #1024바이트 보내고 크기 저장
                    data = f.read(4096) #1024바이트 읽음
    except:
        # 접속이 끊기면 except가 발생한다.
        print("except : " , addr);
    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close();
# 소켓을 만든다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
# 소켓 레벨과 데이터 형태를 설정한다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1);
# 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
# 포트는 pc내에서 비어있는 포트를 사용한다. cmd에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
server_socket.bind(('0.0.0.0', 9090));
# server 설정이 완료되면 listen를 시작한다.
server_socket.listen();
try:
# 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
    while True:
        # client로 접속이 발생하면 accept가 발생한다.
        # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
        client_socket, addr = server_socket.accept();
        # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
        th = threading.Thread(target=binder, args = (client_socket,addr));
        th.start();
except:
    print("server");
finally:
    # 에러가 발생하면 서버 소켓을 닫는다.
    server_socket.close();
