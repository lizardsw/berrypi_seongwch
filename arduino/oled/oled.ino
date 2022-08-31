#include "oled.h"
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);



/* 이거 왜있는지는 몰루...
const int epd_bitmap_allArray_LEN = 1;
const unsigned char* epd_bitmap_allArray[1] = {
	epd_bitmap_ROBOT
};
*/

extern char contain;

void setup() {
	Serial.begin(9600);

  	if(!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
    	Serial.println(F("SSD1306 allocation failed"));
    	for(;;); // Don't proceed, loop forever
  	}
	display.display();
  	display.clearDisplay();
  	delay(1000);

	Wire.begin(SLAVE);
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
1. 눈감기
2. 화내기
3. 울기
4. xx
5. 웃기
*/
void loop() {
	
	
	if(contain == 0)
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
	else
	{
		if(contain == '1')
		{
			show_image(&display, eyes_closed);
			my_delay(4000);
		}
		else if (contain == '2')
		{
			show_image(&display, eyes_sad);
			my_delay(4000);
		}
		else if (contain == '3')
		{
			show_image(&display, eyes_angry);
			my_delay(4000);
		}
		else if (contain == '4')
		{
			show_image(&display, eyes_happy);
			my_delay(4000);
		}
		contain = 0;
	}

}

void receiveFromMaster(int bytes) {
	char ch[2];
	for (int i = 0 ; i < bytes ; i++) {
		// 수신 버퍼 읽기
		ch[i] = Wire.read(); 
	}
	contain = ch[0];
	Serial.println(contain);
	digitalWrite(3, HIGH);
	delay(300);
	digitalWrite(3, LOW);
}

void sendToMaster() {
	// 자신의 슬레이브 주소를 담은 메세지를 마스터에게 보냅니다. 슬레이브 주소에 맞게 수정해야 합니다.
	Wire.write("4th Arduino ");
}

void testdrawchar(char c) {
  display.clearDisplay();

  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.cp437(true);         // Use full 256 char 'Code Page 437' font
	display.write(c);
  display.display();
  delay(2000);
}


void my_delay(int time)
{
	int i = 0;
	while(i < time)
	{
		if (contain != 0)
			break;
		delay(1);
		i++;
	}
}


/*
void eyes_cross()
{
	scrolling(25, -17, epd_bitmap_ROBOT, 5, 5);
	scrolling(-25, -17, epd_bitmap_ROBOT, 5, 5);
	scrolling(25, 17, epd_bitmap_ROBOT, 5, 5);
}

void eyes_earth_quake(int time)
{
	for (int i = 0; i < time; i++)
	{
		scrolling(10, 0, epd_bitmap_ROBOT, 5, 5);
		delay(200);
		scrolling(-10, 0, epd_bitmap_ROBOT, 5, 5);
		delay(200);
	}
}

*/