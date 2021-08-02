from urllib.request import urlopen
import socket
import time
from

#from nestorestream import nestore
from tangible_server import start_server


def CHECK_CONNECTION():   #at first you need to check if there is wifi connection
    connected=False
    while not connected:
        try: 
            socket.setdefaulttimeout(23)
            response=  urlopen("http://www.google.com")
            print(response)

        except:
            print("network down")
           
            connected= False
            os.system("aplay -D hw:2,1 /home/pi/nestore/connection_unsucessful.wav")
            led.set([{},'blue','blue','blue',{},{},'blue','blue','blue',{},{},{},{},{},'blue','blue','blue',{}])  #call bluetooth
            start_server()
        else:
            connected=True
            print("up")


if __name__ == '__main__':
	CHECK_CONNECTION()


