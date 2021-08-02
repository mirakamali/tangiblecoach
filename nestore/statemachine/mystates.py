# my_states.py
import time
import threading
from state import State



import board
import digitalio
import busio
import adafruit_lis3dh

# Start of our states
import sys
sys.path.append("/home/pi/nestore")
from chargelevel import getchargelevel
from mainscript import CHECK_CONNECTION  
sys.path.append("/home/pi/nestore/snowboy/examples/Python3")
import snowboydecoder
import board
import digitalio
import busio
import adafruit_lis3dh
import signal
import os
i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

global interrupted
interrupted= False
import multiprocessing
from matrix_lite import led
def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    if(lis3dh.acceleration[2]>9 and lis3dh.acceleration[2]<10.2): 
          return True

signal.signal(signal.SIGINT, signal_handler)
detector= None
def f():  
          CHECK_CONNECTION()
          
  
          getchargelevel()
          TOP_DIR = os.path.dirname(os.path.abspath(__file__))
          model = os.path.join(TOP_DIR, "wakeword/nestore.pmdl")
          detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
   
          return detector

       
       

#process= multiprocessing.Process(target=f)


class SleepState(State):
    """
    The state which indicates that there are limited device capabilities.
    """
    def __init__(self):
        
            
             
 
               led.set("black")

         

    def on_event(self, event):
        if event == 'wakeup':
         ###   self.interrupted= False    ##sleep to wake
                            
               
               return WakeState()

        return self


class WakeState(State):
    """
    The state which indicates that there are no limitations on device
    capabilities.
    """
    def __init__(self):
         
            print("i am at init")
          # self.process= multiprocessing.Process(target=f, daemon=True)
          
           
           
          # self.process.start()
            CHECK_CONNECTION()
          
  
            getchargelevel()
            TOP_DIR = os.path.dirname(os.path.abspath(__file__))
            model = os.path.join(TOP_DIR, "wakeword/nestore.pmdl")
            detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
       
        
          # detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
            detector.start(detected_callback=detector.play_audio_file, interrupt_check=interrupt_callback,sleep_time=0.03) 
            detector.terminate() 
          

        
    def on_event(self, event):
        if event == 'sleep':
            
           # self.process.terminate()
          #  self.process.join()
     
          ###wake to sleep
            return SleepState()

        return self
  
# End of our states.
