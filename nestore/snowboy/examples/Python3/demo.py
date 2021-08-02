import snowboydecoder
import sys
import signal
import os
#interrupted = False
#from mystates import interrupted
import time
interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
  #  global interrupted
   # return interrupted
    if(lis3dh.acceleration[2]>9 and lis3dh.acceleration[2]<10.2): 
        return True
  #  global interrupted
    #time.sleep(2)
   # if(wake.getinterrupt()== True):
       
 #   print("from interrupt callback"+ str(interrupted))
     #  return True

#if len(sys.argv) == 1:
 #   print("Error: need to specify model name")
  #  print("Usage: python demo.py your.model")
  #  sys.exit(-1)

#model = sys.argv[1]
TOP_DIR = os.path.dirname(os.path.abspath(__file__))
model = os.path.join(TOP_DIR, "resources/models/nestore.pmdl")
# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

#callbacks=[lambda: nestoreconv.conversation()]

print("Listening... Press Ctrl+C to exit")
if __name__ == '__main__':
   detector.start(detected_callback=detector.play_audio_file,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

   detector.terminate()
