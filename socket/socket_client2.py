import socket

HOST = 'localhost'
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) # 연결 
    while True:
        n = input("1-9 사이의 숫자를 입력하세요(0은 게임포기):")
        if not n.strip():
            print("입력값이 잘못되었습니다.")
            continue
        s.sendall(n.encode('utf-8')) ## 송신
        data = s.recv(1024).decode('utf-8') ## 수신
        print(f'서버응답:{data}')
        if data == "정답" or data == "종료":
            break