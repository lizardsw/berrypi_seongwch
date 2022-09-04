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

print('Moving servo on channel 0, press Ctrl-C to quit...')
while True:
    # Move servo on channel O between extremes.
    data = int(input("input :"))
    set_angle(pwm, 0, data)
    # pwm.set_pwm(0, 0, data)
    # pwm.set_pwm(0, , servo_max)

