from ssd1306 import SSD1306_I2C
from bmp280 import *
import machine
import utime

# init internal temperature sensor
sensor = machine.ADC(4)
CONVERSION_FACTOR = 3.3 / 65535

# init i2c communication
sda=machine.Pin(0)
scl=machine.Pin(1)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=400000)

# init oled display
WIDTH = 128
HIGHT = 64
oled = SSD1306_I2C(WIDTH, HIGHT, i2c)

# init bmp280
bmp = BMP280(i2c)

# global variables
temp = 0
internal_temp = 0
pressure = 0
status_text = ""
    
def show_i2c_addresses(i2c):
    addresses = i2c.scan()
    
    for i in range(len(addresses)):
        print(f"I2C address {i}: {hex(addresses[i]).upper()}")
        
def read_internal_temp(sensor, factor):
    value  = sensor.read_u16() * factor
    
    return 27 - (value - 0.706) / 0.001721

def main_devices():
    # assign global variables for working multi threaded code
    global temp
    global internal_temp
    global pressure
    
    i = 0
    while True:
        # read values
        temp = bmp.temperature
        pressure = bmp.pressure
        internal_temp = read_internal_temp(sensor,CONVERSION_FACTOR)
        
        # debug
        print(f"BMP280: {temp}, Pressure BMP280: {pressure}, Temperature Pico: {internal_temp}")
        print(f"Counter: {i}")

        # show values on oled
        oled.fill(0)
        oled.text('Temp: ',0,8)
        oled.text(str(round(temp,2)),44,8)
        oled.text('*C',89,8)
        
        #oled.text('Temp: ',0,22)
        #oled.text(str(round(internal_temp,2)),44,22)
        #oled.text('*C',89,22)
        
        oled.text('Pres:',0,22)
        oled.text(str(round(pressure)),44,22)
        oled.text("pa",89,22)
        
        oled.text(status_text,0,50)
        
        oled.show()
        i+=1
        utime.sleep(2)


if __name__ == "__main__":
    # init debug led
    led = machine.Pin("LED",machine.Pin.OUT)
    led.on()
        
    show_i2c_addresses(i2c)
    main_devices()