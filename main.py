from devices import main_devices, oled
from html import html
from secrets import SSID, PASSWORD

import devices

from machine import Pin

import framebuf
import network
import socket
import time
import _thread

#wlan = network.WLAN(network.STA_IF)

def create_wifi():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)
    
    status = ap.ifconfig()
    devices.status_text = "ip" + status[0]

def connect_to_wifi():
    print("connection triggered")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140)
    wlan.connect(SSID, PASSWORD)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    if wlan.status() != 3:
        print("no network connection")
        
        # debug message on oled
        oled.fill(0)
        oled.text('Network',0,8)
        oled.text('connection',0,22)
        oled.text('failed!',0,36)
        oled.show()
        
        devices.status_text = "No Wifi!"
        
        time.sleep(1)

        #raise RuntimeError('network connection failed')
        wlan.active(False)
    
    else:
        print('connected')
        status = wlan.ifconfig()
        
        print( 'ip = ' + status[0] )
        devices.status_text = "ip" + status[0]
        
def handle_requests():
    # setup webserver
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)

    # listen for connections
    while True:
        #print("hello world")
        
        try:
            cl, addr = s.accept()
            print('client connected from', addr)
            request = cl.recv(1024)
            print(request)

            request = str(request)
            data_url = request.find('/data')
            
            print(data_url)
            
            # serve data
            if data_url == 6:
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plane\r\n\r\n')
                cl.send(f"{devices.temp} {devices.pressure}")
                cl.close()
            
            # serve static html
            else:
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(html)
                cl.close()

        except OSError as e:
            cl.close()
            print('connection closed')
        
if __name__ == "__main__":
    led = Pin("LED", Pin.OUT)
    led.on()
    
    buffer = bytearray(b'\x1f\xe0\x00\x00?\xf0\x00\x00?\xf0\x00\x008p\x00\x00;p\xc0\x0030\xc0\x0030\xc0\x0030\xc1\xc030\x03\xc030\x03\xc030\xfb\x8030\xfc\x0030~\x0030\x1e\x0030\x0e\x0030\x0ex30\x0ex30\x0e\x0030\x1e\x0030~\x00s8\xfc\x00\xf3<\xfb\x80\xff\xfc\x03\xc0\xef\xdc\x03\xc0\xef\xdc\xc1\xc0\xef\xdc\xc0\x00\xef\xdc\xc0\x00\xef\xdc\xc0\x00\xf0<\x00\x00\x7f\xf8\x00\x00?\xf0\x00\x00\x1f\xe0\x00\x00')
    
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
    oled.fill(0)
    oled.blit(fb, 48, 16)
    oled.show()
    time.sleep(2)
    
    devices.show_i2c_addresses(devices.i2c)
    time.sleep(1)
    
    connect_to_wifi()
    #create_wifi()
    led.off()
    
    _thread.start_new_thread(main_devices,())
    
    handle_requests()
        