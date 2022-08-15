import socket
import select
import random
import time
import signal
import sys


HOST = ''
PORT = 50008


def init_socket(sock, readsocks, socket_dict):
	newsock, addr = sock.accept()
	data = newsock.recv(1024).decode('utf-8')
	readsocks.append(newsock)
	newsock.sendall("완료!".encode('utf-8'))
	socket_dict[newsock] = data
	# print(socket_dict)

def get_key(my_dict, my_value):
	for x, y in my_dict.items() :
		if y == my_value:
			return x
	return -1

def str_to_dict(dict_str):
	split_data = dict_str.split(";")
	my_dict = {}
	for x in split_data :
		if (x != ""):
			temp = x.split('=')
			my_dict[temp[0]] = int(temp[1])
	return my_dict

def dict_to_str(my_dict):
	dict_str = ""
	for x, y in my_dict.items() :
		dict_str += str(x)
		dict_str += "="
		dict_str += str(y)
		dict_str += ";"
	return (dict_str)

face_locate = {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
	s.bind((HOST, PORT)) # 소켓을 주소, 포트와 연결
	s.listen() # 연결을 기다림
	print("서버 시작!") 
	readsocks = [s]
	socket_dict = {}
	while True :
		readables, writeables, exceptions = select.select(readsocks, [], [])
		for sock in readables:
			if sock == s:
				init_socket(sock, readsocks, socket_dict)
			else :
				if (socket_dict[sock] == "opencv") : 
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					#print("opencv" + data)
					data = str_to_dict(data)
					face_locate['x'] = data['x']
					face_locate['y'] = data['y']
					print(data)
					print(face_locate)
					data = dict_to_str(face_locate)
					servo_cnn = get_key(socket_dict, "servo")
					if (servo_cnn != -1) :
						servo_cnn.sendall(data.encode('utf-8'))
				elif (socket_dict[sock] == "servo") :
					conn = sock
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					print("servo" + data)
					


