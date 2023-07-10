import machine
from machine import Pin,PWM
Trigger = Pin(21, Pin.OUT)
Echo = Pin(22, Pin.IN)

import utime
from utime import sleep, sleep_us, ticks_us, sleep_ms
from machine import Pin, PWM
from ili934xnew import ILI9341, color565
from machine import  SPI
from micropython import const
import os
import glcdfont
import tt14
import tt24
import tt32
import time

# Dimenzije displeja
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)
CENTER_Y = int(SCR_WIDTH/2)
CENTER_X = int(SCR_HEIGHT/2)

print(os.uname())

# Podešenja SPI komunikacije sa displejem
TFT_CLK_PIN = const(18)
TFT_MOSI_PIN = const(19)
TFT_MISO_PIN = const(16)
TFT_CS_PIN = const(17)
TFT_RST_PIN = const(20)
TFT_DC_PIN = const(15)

# Fontovi na raspolaganju
fonts = [glcdfont,tt14,tt24,tt32]

text = 'RPi Pico/ILI9341'

print(text)
print("Fontovi:")
for f in fonts:
    print(f.__name__)

spi = SPI(
    0,
    baudrate=62500000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN))

print(spi)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT)

# Brisanje displeja i odabir pozicije (0,0)
display.erase()
display.set_pos(0,0)

# Ispis teksta različitim fontovima, počevši od odabrane pozicije
for ff in fonts:
    display.set_font(ff)

display.set_font(tt32)
display.erase()

Trigger.value(0)
class Servo:
    """ A simple class for controlling a 9g servo with the Raspberry Pi Pico.
 
    Attributes:
 
        minVal: An integer denoting the minimum duty value for the servo motor.
 
        maxVal: An integer denoting the maximum duty value for the servo motor.
 
    """
 
    def __init__(self, pin: int or Pin or PWM, minVal=2500, maxVal=7500):
        """ Creates a new Servo Object.
 
        args:
 
            pin (int or machine.Pin or machine.PWM): Either an integer denoting the number of the GPIO pin or an already constructed Pin or PWM object that is connected to the servo.
 
            minVal (int): Optional, denotes the minimum duty value to be used for this servo.
 
            maxVal (int): Optional, denotes the maximum duty value to be used for this servo.
 
        """
 
        if isinstance(pin, int):
            pin = Pin(pin, Pin.OUT)
        if isinstance(pin, Pin):
            self.__pwm = PWM(pin)
        if isinstance(pin, PWM):
            self.__pwm = pin
        self.__pwm.freq(50)
        self.minVal = minVal
        self.maxVal = maxVal
 
    def deinit(self):
        """ Deinitializes the underlying PWM object.
 
        """
        self.__pwm.deinit()
 
    def goto(self, value: int):
        """ Moves the servo to the specified position.
 
        args:
 
            value (int): The position to move to, represented by a value from 0 to 1024 (inclusive).
 
        """
        if value < 0:
            value = 0
        if value > 1024:
            value = 1024
        delta = self.maxVal-self.minVal
        target = int(self.minVal + ((value / 1024) * delta))
        self.__pwm.duty_u16(target)
 
    def middle(self):
        """ Moves the servo to the middle.
        """
        self.goto(512)
 
    def free(self):
        """ Allows the servo to be moved freely.
        """
        self.__pwm.duty_u16(0)


s1=Servo(28)      # Servo pin is connected to GP0

def servo_Map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
 
def servo_Angle(angle):
    if angle < 0:
        angle = 0
    if angle > 180:
        angle = 180
    s1.goto(round(servo_Map(angle,0,180,0,1024))) # Convert range value to angle value
n=0
def ultra(p):
    global n
    Trigger.high()
    sleep_us(3)
    Trigger.low()
    while Echo.value() == 0:
        signaloff = ticks_us()
    while Echo.value() == 1:
        signalon = ticks_us()
    timepassed = signalon - signaloff
    print(timepassed)
    distance = (timepassed * 0.0343) / 2
    if distance>=30 and distance<45 and n==0:
        n=1
        print("Turn left ...")
        for i in range(360,0,-10):
            servo_Angle(i)
            utime.sleep(0.05)
    else:
        if n==1:
            n=0
            utime.sleep(7)
            for i in range(0,360,10):
                servo_Angle(i)
                utime.sleep(0.05)
            while 1:
               slobodnomjesto(0)
   
 
def slobodnomjesto(p):
    Trigger.high()
    sleep_us(1)
    Trigger.low()
    while Echo.value() == 0:
        signaloff = ticks_us()
    while Echo.value() == 1:
        signalon = ticks_us()
    timepassed = signalon - signaloff
    print(timepassed)
    distance = (timepassed * 0.0343) / 2
    print("The distance from object is ",distance,"cm")
    if distance>55:
        display.set_pos(10,100)
        display.rotation=3
        display.init()
        display.print('Parking prazan')
        time.sleep(2)
        display.erase()
    else:
        display.set_pos(10,100)
        display.rotation=3
        display.init()
        display.print('Parking pun')
        time.sleep(2)
        display.erase()
   
   
if __name__ == '__main__':
    slobodnomjesto(0)
    while True:
        ultra(0)