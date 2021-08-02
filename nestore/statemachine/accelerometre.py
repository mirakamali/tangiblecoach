#import faulthandler; faulthandler.enable()
import numpy
import board
import digitalio
import busio
import adafruit_lis3dh
import time
import threading
import sys
sys.path.append("/home/pi/nestore/statemachine")
from nestore_state_machine import NestoreSM
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)
stateacc= NestoreSM()



def wake_to_sleep():
           if(lis3dh.acceleration[2]>8 and lis3dh.acceleration[2]<11): 

                
                print(stateacc.state)
                event= "sleep"
                stateacc.on_event(event)
                
                 
                 
           else:
  
                
                print(stateacc.state)
                event = "wakeup"
                stateacc.on_event(event)
      


while True:
	wake_to_sleep()
	time.sleep(2)

