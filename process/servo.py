import socket

HOST = 'localhost'
PORT = 50008

def init_socket(s):
    s.connect((HOST, PORT))
    sock_type = "servo"
    s.sendall(sock_type.encode('utf-8'))
    end = s.recv(1024).decode('utf-8')
    print(end)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	init_socket(s)
	while True :
		data = s.recv(1024).decode('utf-8')
		print(data)

