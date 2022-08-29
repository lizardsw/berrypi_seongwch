


def init_socket(sock, readsocks, socket_dict):
	newsock, addr = sock.accept()
	data = newsock.recv(1024).decode('utf-8')
	readsocks.append(newsock)
	newsock.sendall("완료!".encode('utf-8'))
	socket_dict[newsock] = data
	# print(socket_dict)

def get_key(my_dict, my_value):
	for x, y in my_dict.items() :
		if y == my_value:
			return x
	return -1

def str_to_dict(dict_str):
	split_data = dict_str.split(";")
	my_dict = {}
	for x in split_data :
		if (x != ""):
			temp = x.split('=')
			my_dict[temp[0]] = int(temp[1])
	return my_dict

def dict_to_str(my_dict):
	dict_str = ""
	for x, y in my_dict.items() :
		dict_str += str(x)
		dict_str += "="
		dict_str += str(y)
		dict_str += ";"
	return (dict_str)