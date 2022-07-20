# bmp280-sensor/turbo-couscous

![hardware](https://github.com/jolsfd/bmp280-sensor/blob/main/assets/hardware.jpg)
![web page](https://github.com/jolsfd/bmp280-sensor/blob/main/assets/screenshot.png)

# Description

This project aims to read a good quality temperature reading from a sensor and to display this information on an oled screen. In addition to this the new capabilities of the Raspberry Pi Pico W are used to serve a web page with the temperature readings and show different colors based on the temperature. The software also is reading the current air pressure and is showing the information on the display and the web page.

# Parts

* pico w
* oled display 128*64 (ssd1306)
* bmp280

# Credits

* [micropython-bmp280](https://github.com/Dafvid/micropython-bmp280)
* [micropython-ssd1306](https://github.com/stlehmann/micropython-ssd1306)
* [micropython](https://micropython.org/)
* [img2bytearray](https://github.com/novaspirit/img2bytearray)
* [Blog](https://www.az-delivery.de/blogs/azdelivery-blog-fur-arduino-und-raspberry-pi/wetterstation-mit-raspberry-pi-pico-und-oled-display)
* [Icons](https://icons.getbootstrap.com/icons/thermometer-sun/)

# Installation

* permission to write to pico w `chmod a+rw /dev/ttyACM0`
* copy `*.py` files to the internal storage of the pico
* install lib `micropython-ssd1306` with `upip`
* move files from `micropython-bmp280` to the internal storage
* enter your wifi credentials in `secrets.py`
* navigate to the ip that is shown on the oled display
* be happy :)🎉