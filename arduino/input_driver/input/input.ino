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
unsigned int		no_touch = 0;
unsigned int		ir_left_count = 0;
unsigned int		ir_right_count = 0;
int		pre_state[3] = {0, 0, 0};
int		cur_state[3] = {0, 0, 0};
int 	sensor_flag[3]; // [0] -> touch_flag [1] -> left_pir [2] -> right_pir

int sending_serial(int flag)
{
	Serial.print("flag=");
	Serial.print(flag);
	Serial.print(";touch=");
	Serial.print(cur_state[0]);
	Serial.print(";left=");
	Serial.print(cur_state[1]);
	Serial.print(";right=");
	Serial.println(cur_state[2]);
}

int check_flag()
{
	int	i = 0;
	
	if (cur_state[i] - pre_state[i] == 1)
		return (1);
	i++;
	while (i < 3)
	{
		if (cur_state[i] - pre_state[i] == 1)
			return (2);
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
	{
		cur_state[0] = 1;
		no_touch = 0;
	}
	else
	{
		cur_state[0] = 0;
		no_touch++;
	}
	if (cur_state[1] == 1)
		ir_left_count++;
	else 
		ir_left_count = 0;
	if (cur_state[2] == 1)
		ir_right_count++;
	else 
		ir_right_count = 0;
	if (check_flag() == 1)
		sending_serial(0);
	else if (no_touch == 10)
		sending_serial(0);
	else if (check_flag() == 2)
		sending_serial(1);
	else if (ir_left_count == 20)
	{
		ir_right_count += 100;
		cur_state[1] = 2;
		sending_serial(1);
		cur_state[1] = 1;
	}
	else if (ir_right_count == 20)
	{
		ir_right_count += 100;
		cur_state[2] = 2;
		sending_serial(1);
		cur_state[2] = 1;
	}
	pre_state[0] = cur_state[0];
	pre_state[1] = cur_state[1];
	pre_state[2] = cur_state[2];
	delay(100);
}