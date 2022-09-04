import time
import socket
import schedule
import datetime
import pandas as pd
	

HOST = 'localhost'
PORT = 50008


def init_socket(s):
    s.connect((HOST, PORT))
    sock_type = "schedule"
    s.sendall(sock_type.encode('utf-8'))
    end = s.recv(1024).decode('utf-8')
    print(end)

def check_time(time_str) :
	dateformat = "%Y-%m-%d %H:%M:%S"
	time1 = datetime.datetime.now()
	now_time = time1.strftime(dateformat)
	now_time = datetime.datetime.strptime(now_time, dateformat)
	time2 = datetime.datetime.strptime(time_str, dateformat)
	time_diff = (now_time - time2).seconds / 60
	return (int(time_diff))

def check_input_data(s):
	fd_read = open("./input_data.csv") # data_input fd 값 open read
	data = pd.read_csv(fd_read, index_col = 'time')
	time_str = data.index[-1]
	fd_read.close
	time_diff = check_time(time_str)
	print(time_diff)
	s.sendall(str(time_diff).encode('utf-8'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
	init_socket(s)
	schedule.every(4).seconds.do(check_input_data, s)
	#schedule.every(1).minutes.do(check_input_data, s)
	while True:
		schedule.run_pending()
		time.sleep(1)


