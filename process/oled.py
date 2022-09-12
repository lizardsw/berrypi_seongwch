import serial,time
import socket
import datetime
	
my = []

HOST = 'localhost'
PORT = 50008

def init_socket(s):
	s.connect((HOST, PORT))
	sock_type = "oled"
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

def send_time_now():
	data = datetime.datetime.now()
	print(data)
	now = str(data.time())
	print(now)
	now_time = now.split(":")
	return (now_time)


print('Running. Press CTRL-C to exit.')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
	init_socket(s)
	with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
		time.sleep(0.1) #wait for serial to open
		if arduino.isOpen() :
			print("{} connected!".format(arduino.port))
			try:
				while True:
					data = s.recv(1024).decode('utf-8')
					data = str_to_dict(data)
					print(data)
					if (data["flag"] == 0) :
						arduino.write(str(data["value"]).encode())  
					elif (data["flag"] == 1) :
						arduino.write(str(data["value"]).encode())
						time.sleep(int(data['time']))
						arduino.write("0".encode())
					elif (data['flag'] == 2):
						arduino.write(str(data["value"]).encode()) 
						now_time = send_time_now()
						arduino.write(now_time[0][0].encode())
						time.sleep(0.1)
						arduino.write(now_time[0][1].encode())
						time.sleep(0.1)	
						arduino.write(now_time[1][0].encode())
						time.sleep(0.1)
						arduino.write(now_time[1][1].encode())
			except KeyboardInterrupt:
				print("KeyboardInterrupt has been caught.")

