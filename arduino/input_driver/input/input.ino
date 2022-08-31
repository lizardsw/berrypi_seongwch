#include <CapacitiveSensor.h>

/* noano protocol
pir_left: (0,1,2) , pir_right : (0,1,2) , touch : (0,1,2) 

*/

CapacitiveSensor touch_input = CapacitiveSensor(4,5);
#define LEFT_PIR_PIN 2
#define RIGHT_PIR_PIN 3


long	touch_sensor;
int		left_pir_sensor;
int		right_pir_sensor;
int		pre_state[3] = {0, 0, 0};
int		cur_state[3] = {0, 0, 0};
int 	sensor_flag[3]; // [0] -> touch_flag [1] -> left_pir [2] -> right_pir

int sending_serial()
{
	Serial.print("touch=");
	Serial.print(cur_state[0]);
	Serial.print(";left=");
	Serial.print(cur_state[1]);
	Serial.print(";right=");
	Serial.println(cur_state[2]);
}

int check_flag()
{
	int	i = 0;

	while (i < 3)
	{
		if (cur_state[i] - pre_state[i] == 1)
			return (1);
		i++;
	}
	return (0);
}

void setup()
{
	Serial.begin(9600);
	pinMode(LEFT_PIR_PIN, INPUT);    // 센서값을 입력으로 설정
	pinMode(RIGHT_PIR_PIN, INPUT);    // 센서값을 입력으로 설정
}
 
void loop () {
	cur_state[1] = digitalRead(LEFT_PIR_PIN);  // 센서값 읽어옴
	cur_state[2] = digitalRead(RIGHT_PIR_PIN);
	touch_sensor = touch_input.capacitiveSensorRaw(30);
	if (touch_sensor > 1000)
		cur_state[0] = 1;
	else
		cur_state[0] = 0;
	if (check_flag() == 1)
		sending_serial();
	pre_state[0] = cur_state[0];
	pre_state[1] = cur_state[1];
	pre_state[2] = cur_state[2];
	delay(100);
}