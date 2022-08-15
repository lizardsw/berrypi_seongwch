from __future__ import division 
from servo_util import set_angle
import socket
import Adafruit_PCA9685

HOST = 'localhost'
PORT = 50008
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

current_servo_x = 90
current_servo_y = 50

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

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	init_socket(s)
	while True :
		data = s.recv(1024).decode('utf-8')
		data = str_to_dict(data)
		if (abs(data['x']) > 30) :
			if (data['x'] < 0) :
				current_servo_x += 1
				set_angle(pwm, 0, current_servo_x)
			else :
				current_servo_x -= 1
				set_angle(pwm, 0, current_servo_y)
		if (abs(data['y']) > 30) :
			if (data['y'] < 0) :
				current_servo_y += 1
				set_angle(pwm, 1, current_servo_y)
			else :
				current_servo_y -= 1
				set_angle(pwm, 1, current_servo_y)

		


