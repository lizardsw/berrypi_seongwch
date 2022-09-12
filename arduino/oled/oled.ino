#include "oled.h"
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);



/* 이거 왜있는지는 몰루...
const int epd_bitmap_allArray_LEN = 1;
const unsigned char* epd_bitmap_allArray[1] = {
	epd_bitmap_ROBOT
};
*/

int contain;
int time[4] = {0,0,0,0};
int incomingByte = 0;
int flag = 0;
char str_time[6];
void setup() {
	Serial.begin(9600);

  	if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    	Serial.println(F("SSD1306 allocation failed"));
    	for(;;); // Don't proceed, loop forever
  	}
	display.display();
  	display.clearDisplay();
  	delay(1000);

	Wire.begin(0x8);
	//Wire.onReceive(recvData);
	Wire.onReceive(receiveFromMaster);
	Wire.onRequest(sendToMaster);

	if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) 
	{
    	Serial.println(F("SSD1306 allocation failed"));
    	for(;;); // Don't proceed, loop forever
  	}
	pinMode(3, OUTPUT);
	digitalWrite(3, LOW);
	contain = 0;
}
/*
int 값을 넣어주는데..
0. 일반
1. 눈굴리면서 눈깜빡이기
2. 눈감기
3. 슬픔
4. 화남
5. xx
6. 웃기
7. 애교 
*/
void loop() {
	
	
	if(contain == 0)
	{	
		blinking(&display);
		my_delay(2000);
	}
	if(contain == 1)
	{	
		int location = random(10);
		if (location <= 1)
			location = -30;
		else if (location >= 8)
			location = 30;
		else
			location = 0;
		show_image(&display, eyes, location);
		my_delay(2000);	
		blinking(&display, location);
	}
	else if(contain == 2)
	{
		show_image(&display, eyes_closed);
		my_delay(4000);
	}
	else if (contain == 3)
	{
		show_image(&display, eyes_sad);
		my_delay(4000);
	}
	else if (contain == 4)
	{
		show_image(&display, eyes_angry);
		my_delay(4000);
	}
	else if (contain == 5)
	{
		show_image(&display, eyes_happy);
		my_delay(4000);
	}
	else if (contain == 6)
	{
		show_image(&display, eye_cute);
		my_delay(4000);
	}
	else if (contain == 7)
	{
		show_image(&display, eyes_love);
		my_delay(4000);
	}
	else if (contain == 8)
	{
		int i = 0;
		int temp = 0;
		while (i < 4)
		{
			if (Serial.available() > 0)
			{
				incomingByte = Serial.read();
				Serial.println(incomingByte);
				temp = incomingByte - 48;
				time[i] = temp;
				i++;
			}
		}
		flag = 0;
		Serial.print(time[0]);
		Serial.print(time[1]);
		Serial.print(":");
		Serial.print(time[2]);
		Serial.println(time[3]);
		str_time[0] = time[0] + 48;
		str_time[1] = time[1] + 48;
		str_time[3] = time[2] + 48;
		str_time[4] = time[3] + 48;
		str_time[2] = ':';
		str_time[5] = '\0';
		show_time(str_time);
		my_delay(2000);
		contain = 0;
	}
	flag = 0;
}

void receiveFromMaster(int bytes) {
	char ch[2];
	for (int i = 0 ; i < bytes ; i++) {
		// 수신 버퍼 읽기
		ch[i] = Wire.read();
		Serial.println(ch[i]);
	}
	contain = ch[0];
	Serial.println(contain);
	//digitalWrite(3, HIGH);
	//delay(300);
	//digitalWrite(3, LOW);
}

void sendToMaster() {
	// 자신의 슬레이브 주소를 담은 메세지를 마스터에게 보냅니다. 슬레이브 주소에 맞게 수정해야 합니다.
	Wire.write("4th Arduino ");
}



void my_delay(int time)
{
	int i = 0;
	while(i < time)
	{
		if (Serial.available() > 0) 
		{
			incomingByte = Serial.read();
			Serial.println(incomingByte);
			flag = 1;
			contain = incomingByte - 48;
			Serial.print("my_delay catch!");
			Serial.println(contain);
		}
		if (flag == 1)
		{
			return ;
		}
		delay(1);
		i++;
	}
}

void blinking(Adafruit_SSD1306 *display, int x = 0)
{
	int count = random(3);
	
	for (int i = 0; i < count + 1; i++)
	{
		show_image(display, eyes, x);
		my_delay(1000);
		show_image(display, eyes_closed, x);
		my_delay(50);
		if (flag == 1)
			break;
	}
	show_image(display, eyes, x);
	my_delay(50);
}

void show_image(Adafruit_SSD1306 *display, const unsigned char * image, int x = 0, int y = 0)
{
	display -> clearDisplay();
	display -> drawBitmap(x,y,image, 128, 64, 1);
	display -> display();
}

void show_time(char *my_time)
{
	display.clearDisplay();
	display.setTextSize(4);             // Normal 1:1 pixel scale
	display.setTextColor(SSD1306_WHITE);        // Draw white text
	display.setCursor(4,15);             // Start at top-left corner
	display.println(my_time);
	//display.println(F("12:34"));
	display.display();
	Serial.println("show_time!");
}