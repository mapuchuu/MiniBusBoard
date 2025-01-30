## MiniBusBoard 🚌 
### Real-time Bus Arrival Display with ESP32, AWS Lambda, API Gateway, and OneBusAway API

MiniBusBoard is a budget ESP32-powered display that provides live bus arrivals for any stop in Seattle. Unlike standard transit apps, MBB filters out *scheduled* arrivals, so users only see buses that are tied to real buses with updating GPS. This project was inspired by the lack of real-time arrival boards in my metro region. With just $16 worth of hardware, MiniBusBoard brings accurate arrival times to any stop.

 - 1x ESP32 Microcontroller
 - 2x SSD1306OLED Display
 - 1x LCD 16x2 (I2C)
 - 1x Membrane Keypad
 - 1x Potentiometer (optional)
 - 1x any 5V supply

This version works for the Puget Sound region, but it can be configured to work for any of the following transit regions.

 - New York, NY
 - Puget Sound, WA
 - Rogue Valley Transportation District, Oregon
 - San Diego Metropolitan Transit System, California
 - Washington, D.C.
 - Poznań region, Poland
 - Buenos Aires, Argentina
 - Spokane, WA

### Lambda-mmb:
This is the code I used in my Lambda function. To interact with it, you will need to set up a trigger.
A layer is also needed to properly use this function. Lambda free tier includes > 400,000 requests per month.

### ESP32:
This is the code I used in my ESP32 microcontroller. You will need to write in your WiFi SSID and password,
as well as include your own API call to whatever API gateway you make. 

### OledTest:
This is test code for working with your OLED display. I used an SSD1306-based display which had a funky bitmap
output, but you can use this site to change your bitmap format (https://en.radzio.dxp.pl/bitmap_converter/).
Additionally, you may find an issue if your SSD1306 displays have the same address. Most models can have their
addresses changed by resoldering a resistor on the backside. I did not find a software workaround.

### pin_config:
This is a JSON file that outlines which GPIO pins I used for each component. For an ESP32 pin diagram, you 
can visit https://randomnerdtutorials.com/esp32-pinout-reference-gpios/

If you have any questions, feel free to message me on linkedin https://www.linkedin.com/in/matthew-chu-chu/


An OBA API key can be acquired by emailing a request to: oba_api_key@soundtransit.org


