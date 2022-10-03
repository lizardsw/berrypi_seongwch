from __future__ import division 
from servo_util import set_angle
import time
# Import the PCA9685 module.
import Adafruit_PCA9685
# Alternatively specify a different address and/or bus:
pwm = Adafruit_PCA9685.PCA9685(address=0x40, busnum=1)

# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

pwm.set_pwm_freq(60)

current_pulse = [400, 304]

def map(value, min_angle, max_angle, min_pulse, max_pulse):
	angle_range = max_angle - min_angle
	pulse_range = max_pulse - min_pulse
	scale_factor = float(angle_range)/float(pulse_range)
	return min_pulse + (value/scale_factor)

def angle_to_pulse(angle):
	pulse = int(map(angle, 0, 180, servo_min, servo_max))
	print(pulse)
	return (pulse)



def move_angle(pwm, channel, current, target_angle):
	if (target_angle < 0):
		target = -(angle_to_pulse(-target_angle)) + 150
	else :
		target = angle_to_pulse(target_angle) - 150
	current[channel] = current[channel] + target
	pwm.set_pwm(channel, 0, current[channel])

def set_pulse(pwm, channel, pulse):
	pwm.set_pwm(channel, 0, pulse)
	print("####{} : {}".format(channel, pulse))

print('Moving servo on channel 0, press Ctrl-C to quit...')
set_pulse(pwm, 0, current_pulse[0])
set_pulse(pwm, 1, current_pulse[1])
while True:
    # Move servo on channel O between extremes.
    data = int(input("input :"))
    # angle_to_pulse(data)
	# set_(pwm, 0, data)
    move_angle(pwm, 1, current_pulse, data)
    print(current_pulse[0]," ",current_pulse[1])
    # pwm.set_pwm(0, , servo_max)


#if (flag == 0) : 
	#	if (face > 200):
	#		if (data_abs > 50) :
	#			i = 5
	#		elif (data_abs > 100) :
	#			i = 12
	#		elif (data_abs > 150) :
	#			i = 18
	#	else :
	#		if (data_abs > 50) :
	#			i = 3
	#		elif (data_abs > 100) :
	#			i = 7
	#		elif (data_abs > 150) :
	#			i = 10
# else :
	# 	if (face > 200) :
	# 		if (data_abs > 50) :
	# 			i = 4
	# 		elif (data_abs > 70) :
	# 			i = 8
	# 		elif (data_abs > 120) : 
	# 			i = 12
	# 	else :
	# 		if (data_abs > 50) :
	# 			i = 2
	# 		elif (data_abs > 70) :
	# 			i = 4
	# 		elif (data_abs > 120) : 
	# 			i = 7