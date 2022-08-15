import socket

HOST = 'localhost'
PORT = 50008

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
		print(data)


