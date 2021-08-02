## Set Initial Variables ##
import os # Miscellaneous operating system interface
import time # Time access and conversions
from random import randint # Random numbers
import sys # System-specific parameters and functions
from multiprocessing import Process, Manager, Value # Allow for multiple processes at once
import threading
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from matrix_lite import led

class ThreadingLeds(object):  
    def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        thread = threading.Thread(target=self.listen, args=())
        self.next=threading.Event()
        self.queue= Queue.Queue()       
      ##  thread.daemon = True                            # Daemonize thread
      ##  thread.start()  
    def run(self):
    
        """ Method that runs forever """
        while True:
            print("queue", self.queue.get())
            self.queue.get()
            

    def listen_nestore(self):
        #self.next.set()
        self.queue.put(self.listen())
    def think_nestore(self):
        #self.next.set()
        self.queue.put(self.think())       
    def speak_nestore(self):
        #self.next.set()
        self.queue.put(self.speak())
    def off_nestore(self):
       # self.queue.close()
       
        self.queue= Queue.Queue() 
  
        #self.next.set()
        self.queue.put(self.off())      
    def wakeword_nestore(self):
        self.queue.put(self.wakeword())
    def notification_nestore(self):
        self.queue.put(self.notification())
    def wakewording(self):
        self.next.clear()
        led.set([{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'orange'])
		
		
    def listening(self):
        print("listening state")
        time.sleep(0.3)
        self.next.clear()
        self.next.set()
        while self.next.is_set():
          led.set('orange')
        
        
    def thinking(self):
        self.next.set()
        while self.next.is_set():
            led.set(['orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange'])
            time.sleep(0.4)
            led.set([{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange',{},'orange'])
            time.sleep(0.4)
                
    def speaking(self):
        self.next.clear()
        print("speaking state")
        ##self.next.set()
        ###self.next.clear()
        while not self.next.is_set():
        #while self.next.is_set():
            led.set('#ff2500')# Hex values
            time.sleep(0.6)
    # Turns off each LED
            led.set('black') # color name
            time.sleep(0.6)
    def offing(self):
        print("off state")
        self.next.clear()
        self.next.set()
        
        while self.next.is_set():
         led.set("black")
    def lowcharge(self):
          self.next.clear() 
          #needs to be charged de 0 juska 40
          led.set("red")
          time.sleep(1)
          led.set("red")
          time.sleep(0.5)
          led.set("black")  
    def highcharge(self):
          self.next.clear() 
          led.set("green")
          time.sleep(1)
          led.set("green")
          time.sleep(0.5)
          led.set("black")
    def charging(self):
          self.next.clear() 
          led.set("blue")
          time.sleep(1)

          led.set("black")
                #needs to be charged de 90 juska 100
    def mediumcharge(self): #needs to be charged de 40 juska 90
          self.next.clear() 
          led.set("yellow")
          time.sleep(1)
          led.set("yellow")
          time.sleep(0.5)  
          led.set("black")   
    def listen(self):
        thread = threading.Thread(target=self.listening, args=())
        self.next=threading.Event()
        
        thread.daemon = True                            # Daemonize thread
        thread.start()                  
        
    def think(self):
        thread = threading.Thread(target=self.thinking, args=())
        self.next=threading.Event()
        
        thread.daemon = True                            # Daemonize thread
        thread.start()       

        

               
    

    def speak(self):
        thread = threading.Thread(target=self.speaking, args=())
        self.next=threading.Event()
        
        thread.daemon = True                            # Daemonize thread
        thread.start()
       
        
    def off(self):
        thread = threading.Thread(target=self.offing, args=())
        self.next=threading.Event()
        
        thread.daemon = True                            # Daemonize thread
        thread.start()
  
    def wakeword(self):
        thread = threading.Thread(target=self.wakewording, args=())
        self.next=threading.Event()
        
        thread.daemon = True                            # Daemonize thread
        thread.start()  
        
    def notification(self): 
   
    ###' to test    self.queue.join()    
        for i in range(3):
                led.set([{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},'green'])
                time.sleep(0.6)
                led.set([{},{},{},{},{},{},{},{},{},{},{},{},{},'green',{},{},{},{}])
                time.sleep(0.6)
            
        led.set("black")
                    
    def clear(self):
      led.set("black")
    def forceclean(self):
        self.queue= Queue.Queue() 
        led.set("black")
        
pixels= ThreadingLeds()
        

       
        

