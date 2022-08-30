from main_servoer_utils import init_socket, get_key, dict_to_str, str_to_dict
from csv import writer
import socket
import select
import random
import time
import signal
import sys
import schedule
import pandas as pd
import datetime

HOST = ''
PORT = 50008

is_person = 0;
is_face_detect = 0;

face_locate = {}

def write_input_data(fd_append, data):
	now = datetime.datetime.now()
	data_list = [now]
	data_list = data_list + data
	writer_object = writer(fd_append)
	writer_object.writerow(data_list)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
	s.bind((HOST, PORT)) # 소켓을 주소, 포트와 연결
	s.listen() # 연결을 기다림
	print("서버 시작!") 
	readsocks = [s]
	socket_dict = {}
	fd_append = open("./input_data.csv", 'a') # data_input fd값 open write
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
					is_person = 1
					write_input_data(fd_append, ['opencv', 'detect'])
					face_locate['x'] = data['x']
					face_locate['y'] = data['y']
					face_locate['h'] = data['h']
					print(data)
					print(face_locate)
					send_data = dict_to_str(face_locate)
					servo_cnn = get_key(socket_dict, "servo")
					if (servo_cnn != -1) :
						if (data['h'] > 100) :
							servo_cnn.sendall(send_data.encode('utf-8'))
				elif (socket_dict[sock] == 'input') :
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					data = str_to_dict(data)
					print(data)
					write_input_data(fd_append, ['input_driver', 'detect'])
					is_person = 1
				elif (socket_dict[sock] == 'schedule') :
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					print(data)
					print(type(data))
					# if (data > 5):
					# 	is_face_detect = 0
					# 	is_person = 0
				elif (socket_dict[sock] == "servo") :
					conn = sock
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					print("servo" + data)
					


