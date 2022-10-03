from __future__ import division 
from servo_util import set_angle, set_pulse, angle_to_pulse, ear_servo, move_angle, touch_emotion, sleep_emotion
import socket
import Adafruit_PCA9685
import time
import threading
import math

ABS_value = 10
thread_flag = 0
HOST = 'localhost'
PORT = 50008
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)
pwm.set_pwm_freq(60)

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

current_pulse = [400, 304]
face_location = {}
face_location['x'] = 0
face_location['y'] = 0

x_on = 0
y_on = 0
sleep_mode = 0

def sub_thread(x_pulse, y_pulse):
	global thread_flag
	
	while thread_flag == 1 :
		ear_servo(pwm, 110)
		for x in range(0, 10):
			if (thread_flag == 0):
				return
			time.delay(0.1)
		ear_servo(pwm, 40)
		for x in range(0, 10):
			if (thread_flag == 0):
				return
			time.delay(0.1)
	return

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

def setting_i(data_abs, flag, face):
	i = 1
	#if (flag == 0) : 
	#	if (face > 200):
	#		if (data_abs > 50) :
	#			i = 5
	#		elif (data_abs > 100) :
	#			i = 12
	#		elif (data_abs > 150) :
	#			i = 18
	#	else :
	#		if (data_abs > 50) :
	#			i = 3
	#		elif (data_abs > 100) :
	#			i = 7
	#		elif (data_abs > 150) :
	#			i = 10
	if (flag == 0) :
		if (face > 200) :
			i = int(pow((1.2), (data_abs - 10 / 10)))
		else :
			i = int(pow((1.1), (data_abs - 10 / 10))) 
	else :
		if (face > 200) :
			if (data_abs > 50) :
				i = 4
			elif (data_abs > 70) :
				i = 8
			elif (data_abs > 120) : 
				i = 12
		else :
			if (data_abs > 50) :
				i = 2
			elif (data_abs > 70) :
				i = 4
			elif (data_abs > 120) : 
				i = 7
	return i

def detect_face_servo(pwm, data, current_pulse, face_size):
	global x_on
	global y_on
	data_x_abs = abs(data['x'])
	data_y_abs = abs(data['y']) 
	if (data_x_abs > ABS_value and x_on == 0) :
		i = setting_i(data_x_abs, 0, face_size)
		if (data['x'] < 0) :
			current_pulse[0] += i
		else :
			current_pulse[0] -= i
		set_pulse(pwm, 0, current_pulse[0])
	elif (data_x_abs > 100) :
		x_on = 0
	else :
		x_on = 1
	if (data_y_abs > ABS_value and y_on == 0) :
		i = setting_i(data_y_abs, 1, face_size)
		if (data['y'] < 0) :
			current_pulse[1] += i
		else :
			current_pulse[1] -= i
		set_pulse(pwm, 1, current_pulse[1])
	elif (data_y_abs > 60) :
		y_on = 0
	else :
		y_on = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	init_socket(s)
	set_pulse(pwm, 0, current_pulse[0])
	set_pulse(pwm, 1, current_pulse[1])
	i = 0
	while True :
		data = s.recv(1024).decode('utf-8')
		data = str_to_dict(data)
		print(data)
		if (data['emotion'] == 0):
			detect_face_servo(pwm, data, current_pulse, data['h'])
			if (x_on == 1 and y_on == 1):
				s.sendall("1".encode('utf-8'))
			else :
				s.sendall("0".encode('utf-8'))
		elif (data['emotion'] == 1): # emotion express
			if (sleep_mode == 1):
				if (data['value'] == 0 or data['value'] == 3):
					continue
				sleep_mode = 0
				set_pulse(pwm, 1, angle_to_pulse(60))
				current_pulse[1] = angle_to_pulse(60)
			if (data['value'] == 0):
				ear_servo(pwm, 30)
			elif (data['value'] == 1):
				ear_servo(pwm,0)
			elif (data['value'] == 2): # touch 
				if (data['type'] == 1): # start_touch
					thread_flag = 1
					sub_thread = threading.Thread(target = sub_thread)
					sub_thread.daemon = True
					sub_thread.start()
				else :
					thread_flag = 0 # finish_touch
					time.sleep(0.1)
					for x in range(0, 4):
						set_pulse(pwm, x, 0)
					ear_servo(pwm, 30)
			elif (data['value'] == 3): # sleep
				if (sleep_mode != 1):
					sleep_emotion(pwm, current_pulse)
					time.sleep(2.5)
					s.sendall("2".encode('utf-8'))
				else :
					s.sendall("2".encode('utf-8'))
				sleep_mode = 1
			elif (data['value'] == 4): # zero
				for x in range(0, 4):
					set_pulse(pwm, x, 0)
			elif (data['value'] == 5):
				move_angle(pwm, 0, current_pulse, data['angle'])
				set_pulse(pwm, 1, angle_to_pulse(60))
				current_pulse[1] = angle_to_pulse(60)
				time.sleep(2.5)
				s.sendall("2".encode('utf-8'))

