#include "oled.h"

char contain = 0;

void blinking(Adafruit_SSD1306 *display, int x = 0)
{
	int count = random(3);
	
	for (int i = 0; i < count + 1; i++)
	{
		show_image(display, eyes, x);
		my_delay(1000);
		show_image(display, eyes_closed, x);
		delay(50);
	}
	//show_image(display, eyes, x);
	//delay(50);
}

void show_image(Adafruit_SSD1306 *display, const unsigned char * image, int x = 0, int y = 0)
{
	display -> clearDisplay();
	display -> drawBitmap(x,y,image, 128, 64, 1);
	display -> display();
}

/*
void scrolling(Adafruit_SSD1306 *display, int x, int y, const unsigned char * bitmap, int delay_time, int speed)
{
	int count;
	int now_x;
	int now_y;
	now_x = (x - now_eyes_x) / speed;
	now_y = (y - now_eyes_y) / speed;
	count = (abs(now_x) >= abs(now_y)) ? now_x : now_y;
	count = (count >= 0) ? count : -count; 
	for (int i = 1; i <= count + 1; i++)
	{
		display.clearDisplay();
		display.drawBitmap(now_eyes_x + i * (x - now_eyes_x)/count, now_eyes_y + i * (y - now_eyes_y)/count , bitmap, 128, 64, 1);
		display.display();
		delay(delay_time);
	}
	now_eyes_x = x;
	now_eyes_y = y;
}
*/
