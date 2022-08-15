from __future__ import division 
from servo_util import set_angle
import socket
import Adafruit_PCA9685

ABS_value = 20
HOST = 'localhost'
PORT = 50008
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

current_servo_x = 90
current_servo_y = 50

face_location = {}
face_location['x'] = 0
face_location['y'] = 0

def init_socket(s):
	s.connect((HOST, PORT))
	sock_type = "servo"
	s.sendall(sock_type.encode('utf-8'))
	end = s.recv(1024).decode('utf-8')
	print(end)

def str_to_dict(dict_str):
	split_data = dict_str.split(";")
	my_dict = {}
	for x in split_data :
		if (x != ""):
			temp = x.split('=')
			my_dict[temp[0]] = int(temp[1])
	return my_dict

def detect_face_servo(data, current_servo_x, current_servo_y):
	if (abs(data['x']) > ABS_value) :
			if (data['x'] < 0) :
				current_servo_x += 1
				set_angle(pwm, 0, current_servo_x)
			else :
				current_servo_x -= 1
				set_angle(pwm, 0, current_servo_y)
		if (abs(data['y']) > ABS_value) :
			if (data['y'] < 0) :
				current_servo_y += 1
				set_angle(pwm, 1, current_servo_y)
			else :
				current_servo_y -= 1
				set_angle(pwm, 1, current_servo_y)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	init_socket(s)
	set_angle(pwm, 0, current_servo_x)
	set_angle(pwm, 1, current_servo_y)
	i = 0
	while True :
		data = s.recv(1024).decode('utf-8')
		data = str_to_dict(data)
		print(data)
		if (i < 10) :
			face_location['x'] = face_location['x'] * i + data['x']
			face_location['y'] = face_location['y'] * i + data['y']
			i += 1
		else :
			i = 0
			detect_face_servo(face_location, current_servo_x, current_servo_y)
		


