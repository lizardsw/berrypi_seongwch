import serial,time
    
my = []
print('Running. Press CTRL-C to exit.')
with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
    time.sleep(0.1) #wait for serial to open
    if arduino.isOpen():
        print("{} connected!".format(arduino.port))
        try:
            while True:
                # cmd=input("Enter command : ")
                # arduino.write(cmd.encode())
                #time.sleep(0.1) #wait for arduino to answer
                while arduino.inWaiting()==0: pass
                if  arduino.inWaiting()>0: 
                    answer=arduino.readline()
                    print(answer)
                    real = answer[:-2]
                    print(real)
                    my.append(real)
                    print(my)
                    arduino.flushInput() #remove data after reading
        except KeyboardInterrupt:
            print("KeyboardInterrupt has been caught.")