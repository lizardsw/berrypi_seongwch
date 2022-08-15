import cv2

capture = cv2.VideoCapture(-1)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def dict_to_str(my_dict):
	dict_str = ""
	for x, y in my_dict.items() :
		dict_str += str(x)
		dict_str += "="
		dict_str += str(y)
		dict_str += ";"
	return (dict_str)

face_cascade = cv2.CascadeClassifier('haarcascade/haarcascade_frontalface_default.xml')
while 1 :
    ret, frame = capture.read()     # 카메라로부터 현재 영상을 받아 frame에 저장, 잘 받았다면 ret가 참
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 영상을 흑백으로 바꿔줌
    faces = face_cascade.detectMultiScale(gray, scaleFactor= 1.5, minNeighbors=3, minSize=(20,20))
    face_info = {}
    space = 0
    i = 0
    if len(faces) :
        i = len(faces)
        for x, y, w, h in faces :
            if int(w*h) > space :
                space = w*h
                face_info['x'] = x
                face_info['y'] = y
                face_info['w'] = w
                face_info['h'] = h
        face_info['i'] = i
        face_info['x'] = face_info['x'] - 320
        face_info['y'] = face_info['y'] - 240
        data = dict_to_str(face_info)
        print(data)