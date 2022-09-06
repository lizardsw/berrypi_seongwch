import subprocess
import time
import os

subprocess.Popen(["python3", "main_server.py"])
time.sleep(1)
subprocess.Popen(["python3", "oled.py"])
subprocess.Popen(["python3", "servo.py"])
subprocess.Popen(["python3", "schedule_prc.py"])
time.sleep(1)
subprocess.Popen(["python3", "my_serial.py"])
subprocess.Popen(["python3", "opencv.py"])

try:
    while True:
        pass
except KeyboardInterrupt:
    # Ctrl+C 입력시 예외 발생
    subprocess.Popen.terminate()


