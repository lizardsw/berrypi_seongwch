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
import os

HOST = ''
PORT = 50008

is_person = 0
is_face_focus = 0
face_detecting = 0
ir_person = 0
sleep_mode = 0
moving_mode = 0
detect_mode = 0
face_locate = {}
face_locate['emotion'] = 0


def write_input_data(fd_append, data):
	now = datetime.datetime.now()
	dateformat = "%Y-%m-%d %H:%M:%S"
	now = now.strftime(dateformat)
	data_list = [now]
	data_list = data_list + data
	print("@@@@@@@@@@@@@@@@@@input : " ,data_list)
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
					if (moving_mode == 0) : # if moving? no input
						# conn.sendall("ok!".encode('utf-8'))
						data = str_to_dict(data)
						fd_append = open("./input_data.csv", 'a') # data_input fd값 open write
						write_input_data(fd_append, ['opencv', 'detect'])
						fd_append.close
						face_locate['x'] = data['x']
						face_locate['y'] = data['y']
						face_locate['h'] = data['h']
						print(face_locate)
						face_locate['emotion'] = "0"
						send_data = dict_to_str(face_locate)
						servo_cnn = get_key(socket_dict, "servo")
						oled_cnn = get_key(socket_dict, "oled")
						face_detecting = 0
						print("is_face_detect", is_face_focus)
						if (is_face_focus == 1) :
							is_face_focus = 2
							oled_cnn.sendall("flag=1;value=7;time=1;".encode('utf-8'))
						if (data['h'] > 100) :
							servo_cnn.sendall(send_data.encode('utf-8'))
				elif (socket_dict[sock] == 'input') :
					conn = sock
					data = conn.recv(1024).decode('utf-8')
					conn.sendall("ok!".encode('utf-8'))
					data = str_to_dict(data)
					print(data)
					print("sleep:{} moving:{}is_person:{}detect:{}".format(sleep_mode, moving_mode, is_person,face_detecting))
					servo_cnn = get_key(socket_dict, "servo")
					oled_cnn = get_key(socket_dict, "oled")
					if (data['flag'] == 0): #touch sensor
						fd_append = open("./input_data.csv", 'a') # data_input fd값 open write
						write_input_data(fd_append, ['input_driver', 'detect'])
						fd_append.close
						if (data['touch'] == 1) :
							servo_cnn.sendall("emotion=1;value=2;".encode('utf-8'))
							oled_cnn.sendall("flag=0;value=6;".encode('utf-8'))
						elif (data['touch'] == 0) :
							servo_cnn.sendall("emotion=1;value=0;".encode('utf-8'))
							oled_cnn.sendall("flag=0;value=0;".encode('utf-8'))
						is_person = 1
					elif (data['flag'] == 1): #ir sensor
						if (moving_mode == 0) :
							if (sleep_mode == 1):
								if (data['left'] == 2 or data['right'] == 2):
									continue
								fd_append = open("./input_data.csv", 'a') # data_input fd값 open write
								write_input_data(fd_append, ['input_driver', 'detect'])
								fd_append.close
								sleep_mode == 0
							if(data['left'] == 2 or data['right'] == 2): # ear down
								servo_cnn.sendall("emotion=1;value=0;".encode('utf-8'))
								if (ir_person == 1) :
									if (face_detecting == 1) :
										if (data['left'] == 2):
											servo_cnn.sendall("emotion=1;value=5;angle=30".encode('utf-8'))
											moving_mode = 1
										elif (data['right'] == 2) :
											servo_cnn.sendall("emotion=1;value=5;angle=-30".encode('utf-8'))
											moving_mode = 1
								ir_person = 0
							elif(data['left'] == 1):
								servo_cnn.sendall("emotion=1;value=1;".encode('utf-8'))
								oled_cnn.sendall("flag=0;value=0;".encode('utf-8'))
								ir_person = ir_person + 1
							elif(data['right'] == 1):
								servo_cnn.sendall("emotion=1;value=1;".encode('utf-8'))
								oled_cnn.sendall("flag=0;value=0;".encode('utf-8'))
								ir_person = ir_person + 1
							is_person = 1
				elif (socket_dict[sock] == 'schedule') :
					conn = sock
					data = int(conn.recv(1024).decode('utf-8'))
					print(data)
					if (data > 0):
						servo_cnn = get_key(socket_dict, "servo")
						oled_cnn = get_key(socket_dict, "oled")
						is_face_focus = 0
						is_person = 0
						face_detecting = 1
						oled_cnn.sendall("flag=0;value=2;".encode('utf-8'))
						servo_cnn.sendall("emotion=1;value=3;".encode('utf-8'))
						if (sleep_mode == 0) :
							moving_mode = 1
						sleep_mode = 1 # sleep_mode 
					else :
						if (is_face_focus == 2):
							is_face_focus = 1
						if (is_face_focus == 0):
							face_detecting == 1
						sleep_mode = 0 # sleep_mode change
					print("sleep:{} moving:{}is_person:{}".format(sleep_mode, moving_mode, is_person))
				elif (socket_dict[sock] == "servo") :
					conn = sock
					data = int(conn.recv(1024).decode('utf-8'))
					if (data == 0):
						is_face_focus = 0
					elif (data == 1):
						if (is_face_focus != 1 and is_face_focus != 2):
							is_face_focus = 1
							oled_cnn = get_key(socket_dict, "oled")
							conn.sendall("emotion=1;value=4;".encode('utf-8'))
							oled_cnn.sendall("flag=1;value=7;time=1;".encode('utf-8'))
					elif (data == 2):
						print("moving_mode -> 0")
						moving_mode = 0
					


if __name__ == '__main__':
	os.system("python3 oled.py")
	