import time

servo_min = 150  # Min pulse length out of 4096
servo_max = 650  # Max pulse length out of 4096

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(pwm, channel, pulse):
	pulse_length = 1000000    # 1,000,000 us per second
	pulse_length //= 60       # 60 Hz
	print('{0}us per period'.format(pulse_length))
	pulse_length //= 4096     # 12 bits of resolution
	print('{0}us per bit'.format(pulse_length))
	pulse *= 1000
	pulse //= pulse_length
	pwm.set_pwm(channel, 0, pulse)

def map(value, min_angle, max_angle, min_pulse, max_pulse):
	angle_range = max_angle - min_angle
	pulse_range = max_pulse - min_pulse
	scale_factor = float(angle_range)/float(pulse_range)
	return min_pulse + (value/scale_factor)

def set_angle(pwm, channel, angle):
	pulse = int(map(angle, 0, 180, servo_min, servo_max))
	pwm.set_pwm(channel, 0, pulse)
	print("######{} : {} : {}#####".format(channel,angle, pulse))

def set_pulse(pwm, channel, pulse):
	pwm.set_pwm(channel, 0, pulse)
	print("####{} : {}".format(channel, pulse))

def angle_to_pulse(angle):
	pulse = int(map(angle, 0, 180, servo_min, servo_max))
	return (pulse)

def ear_servo(pwm, angle):
	set_angle(pwm, 2, angle)
	set_angle(pwm, 3, 180 - angle)

def move_angle(pwm, channel, current, target_angle):
	if (target_angle < 0):
		target = -(angle_to_pulse(-target_angle))
	else :
		target = angle_to_pulse(target_angle)
	current[channel] = current[channel] + target
	pwm.set_pwm(channel, 0, current[channel])

def touch_emotion(pwm):
	ear_servo(pwm, 110)
	time.sleep(1.5)
	ear_servo(pwm, 40)


def sleep_emotion(pwm, current_pulse):
	ear_servo(pwm, 140)
	set_pulse(pwm, 1, angle_to_pulse(30))
	current_pulse[1] = angle_to_pulse(30)