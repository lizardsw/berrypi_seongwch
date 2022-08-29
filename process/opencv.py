import socket
import cv2

capture = cv2.VideoCapture(-1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')

HOST = 'localhost'
PORT = 50008

def init_socket(s):
    s.connect((HOST, PORT))
    sock_type = "opencv"
    s.sendall(sock_type.encode('utf-8'))
    end = s.recv(1024).decode('utf-8')
    print(end)

def dict_to_str(my_dict):
	dict_str = ""
	for x, y in my_dict.items() :
		dict_str += str(x)
		dict_str += "="
		dict_str += str(y)
		dict_str += ";"
	return (dict_str)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    init_socket(s)
    while True:
        ret, frame = capture.read()     # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 영상을 흑백으로 바꿔줌
        faces = face_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=3, minSize=(20,20))
        face_info = {}
        space = 0
        i = 0
        if len(faces) :
            i = len(faces)
            for x, y, w, h in faces :
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255,255,255), 2, cv2.LINE_4)
                if int(w*h) > space :
                    space = w*h
                    face_info['x'] = x
                    face_info['y'] = y
                    face_info['w'] = w
                    face_info['h'] = h
            face_info['i'] = i
            face_info['x'] = face_info['x'] + int(w/2) - 320
            face_info['y'] = face_info['y'] + int(h/2) - 240
            data = dict_to_str(face_info)
            s.sendall(data.encode('utf-8'))
            data = s.recv(1024).decode('utf-8')
        cv2.imshow("original", frame)   # frame(카메라 영상)을 original 이라는 창에 띄워줌 
        if cv2.waitKey(1) == ord('q'):  # 키보드의 q 를 누르면 무한루프가 멈춤
           break

#capture.release()                   # 캡처 객체를 없애줌
#cv2.destroyAllWindows()             # 모든 영상 창을 닫아줌
