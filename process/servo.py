from __future__ import division 
from servo_util import set_angle, set_pulse
import socket
import Adafruit_PCA9685

ABS_value = 10
HOST = 'localhost'
PORT = 50008
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

current_servo_x = 90
current_servo_y = 60
current_pulse_x = 400
current_pulse_y = 304
face_location = {}
face_location['x'] = 0
face_location['y'] = 0

x_on = 0
y_on = 0

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

def setting_i(data_abs, flag):
	i = 1
	if (flag == 0) : 
		if (data_abs > 50) :
			i = 3
		elif (data_abs > 100) :
			i = 5
		elif (data_abs > 150) :
			i = 10
	else :
		if (data_abs > 50) :
			i = 2
		elif (data_abs > 100) :
			i = 5
		elif (data_abs > 150) : 
			i = 7
	return i

def detect_face_servo(pwm, data):
	global current_pulse_x
	global current_pulse_y
	global x_on
	global y_on
	data_x_abs = abs(data['x'])
	data_y_abs = abs(data['y']) 
	if (data_x_abs > ABS_value and x_on == 0) :
		i = setting_i(data_x_abs, 0)
		if (data['x'] < 0) :
			current_pulse_x += i
		else :
			current_pulse_x -= i
		set_pulse(pwm, 0, current_pulse_x)
	elif (data_x_abs > 100) :
		x_on = 0
	else :
		x_on = 1
	if (data_y_abs > ABS_value and y_on == 0) :
		i = setting_i(data_y_abs, 1)
		if (data['y'] < 0) :
			current_pulse_y += i
		else :
			current_pulse_y -= i
		set_pulse(pwm, 1, current_pulse_y)
	elif (data_y_abs > 100) :
		y_on = 0
	else :
		y_on = 1


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	init_socket(s)
	set_angle(pwm, 0, current_servo_x)
	set_angle(pwm, 1, current_servo_y)
	i = 0
	while True :
		data = s.recv(1024).decode('utf-8')
		data = str_to_dict(data)
		print(data)
		detect_face_servo(pwm, data)
		


