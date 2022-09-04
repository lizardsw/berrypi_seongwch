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

is_person = 0
is_face_detect = 0

face_locate = {}

def write_input_data(fd_append, data):
	now = datetime.datetime.now()
	dateformat = "%Y-%m-%d %H:%M:%S"
	now = now.strftime(dateformat)
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
					data = str_to_dict(data)
					is_person = 1
					fd_append = open("./input_data.csv", 'a') # data_input fd값 open write
					write_input_data(fd_append, ['opencv', 'detect'])
					face_locate['x'] = data['x']
					face_locate['y'] = data['y']
					face_locate['h'] = data['h']
					print(data)
					print(face_locate)
					face_locate['emotion'] = 0
					send_data = dict_to_str(face_locate)
					servo_cnn = get_key(socket_dict, "servo")
					if (servo_cnn != -1) :
						if (data['h'] > 100) :
							servo_cnn.sendall(send_data.encode('utf-8'))
					fd_append.close
				elif (socket_dict[sock] == 'input') :
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					data = str_to_dict(data)
					print(data)
					fd_append = open("./input_data.csv", 'a') # data_input fd값 open write
					write_input_data(fd_append, ['input_driver', 'detect'])
					fd_append.close
					servo_cnn = get_key(socket_dict, "servo")
					oled_cnn = get_key(socket_dict, "oled")
					if (data['touch'] == 1) :
						servo_cnn.sendall("emotion=1;value=1;".encode('utf-8'))
						print("hello!")
						oled_cnn.sendall("6".encode('utf-8'))
						time.sleep(2)
						print("bye!")
						oled_cnn.sendall("0".encode('utf-8'))
						servo_cnn.sendall("emotion=1;value=0;".encode('utf-8'))
					elif(data['left'] == 1):
						servo_cnn.sendall("emotion=1;value=1;".encode('utf-8'))
						time.sleep(2)
						servo_cnn.sendall("emotion=1;value=0;".encode('utf-8'))
					elif(data['right'] == 1):
						servo_cnn.sendall("emotion=1;value=1;".encode('utf-8'))
						time.sleep(2)
						servo_cnn.sendall("emotion=1;value=0;".encode('utf-8'))

					is_person = 1
				elif (socket_dict[sock] == 'schedule') :
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					print(data)
					print(int(data))
					if (data > 5):
						is_face_detect = 0
						is_person = 0
				elif (socket_dict[sock] == "servo") :
					conn = sock
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					print("servo" + data)
					


