import socket
import random
import time

HOST = ''
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
	s.bind((HOST, PORT))
	s.listen()
	print("서버 시작!")
	conn, addr = s.accept()
	print("클라이언트 접속? {} {}".format(conn, addr))
	data = conn.recv(1024).decode('utf-8')
	print("데이터 {}".format(data))
