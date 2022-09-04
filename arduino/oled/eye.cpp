#include "oled.h"

int contain = 0;
int pre_contain = 0;

void blinking(Adafruit_SSD1306 *display, int x = 0)
{
	int count = random(3);
	
	for (int i = 0; i < count + 1; i++)
	{
		show_image(display, eyes, x);
		my_delay(1000);
		show_image(display, eyes_closed, x);
		my_delay(50);
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
//void testdrawchar(char c) {
//  display.clearDisplay();

//  display.setTextSize(1);      // Normal 1:1 pixel scale
//  display.setTextColor(SSD1306_WHITE); // Draw white text
//  display.setCursor(0, 0);     // Start at top-left corner
//  display.cp437(true);         // Use full 256 char 'Code Page 437' font
//	display.write(c);
//  display.display();
//  delay(2000);
//}

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