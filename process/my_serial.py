import serial,time
import socket
    
my = []

HOST = 'localhost'
PORT = 50008


def init_socket(s):
    s.connect((HOST, PORT))
    sock_type = "input"
    s.sendall(sock_type.encode('utf-8'))
    end = s.recv(1024).decode('utf-8')
    print(end)

print('Running. Press CTRL-C to exit.')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
	init_socket(s)
	with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
		time.sleep(0.1) #wait for serial to open
		if arduino.isOpen():
			print("{} connected!".format(arduino.port))
			try:
				while True:
					while arduino.inWaiting()==0: pass
					if  arduino.inWaiting()>0: 
						answer=str(arduino.readline())
						real = answer[2:-5]
						real = real + ";"
						s.sendall(real.encode('utf-8'))
						arduino.flushInput() #remove data after reading
			except KeyboardInterrupt:
				print("KeyboardInterrupt has been caught.")