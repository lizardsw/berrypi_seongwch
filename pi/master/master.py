"""

    i2c Python Example

    Man-Yong Lee <manyong.lee@gmail.com>, 2013

"""
import smbus
import time

class I2CComm(object):
    I2C_BUS_NUM = 1 # 0 for Model B Rev 1.

    def __init__(self):
        self.master = smbus.SMBus(self.I2C_BUS_NUM) # setting!
        self.slave_addr_list = [8] # 슬레이브 주소 목록

    def run(self):
        me = self.master
        on_off = 1000
        while 1:
            print(" {} \n".format(on_off))
            for addr in self.slave_addr_list:
                try:
                    me.write_byte(addr, int(on_off))
                    on_off += 1
                except IOError:
                    pass
            time.sleep(1)

def main():
    i2c = I2CComm()
    i2c.run()

if __name__ == "__main__":
    main()

# END