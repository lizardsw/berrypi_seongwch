#include <Wire.h>

const int my_i2c_addr = 0x8; // 이 부분은 각 장치마다 다르게 변경하여 컴파일/업로드
const int led_pin =  3;

void setup() {
	pinMode(led_pin, OUTPUT);
	Serial.begin(9600);
	Wire.begin(my_i2c_addr);
	Wire.onReceive(recvData);
	//Wire.onRequest(sendData); // 이 부분은 현재 사용하지 않음
}

void loop() {
  delay(100);
}

void recvData(int byte_count) {
	while( Wire.available()) {
		int on_off = Wire.read();
		Serial.println(on_off);
		if (on_off == 1) {
			digitalWrite(led_pin, HIGH);

	} else {
			digitalWrite(led_pin, LOW);
    		}
	}
}

void sendData() {
  Wire.write(1);
}
