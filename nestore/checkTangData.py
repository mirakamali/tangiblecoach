from urllib.request import urlopen
from matrix_lite import led
import time 
import json
import socket


from everloop2 import pixels
from google.cloud import texttospeech

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import os
import wave

os.environ[
   "GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/nestore/credentials.json"


def testconnection():
    
    while True:
        try: 
            socket.setdefaulttimeout(23)
            response=  urlopen("http://www.google.com")
         
        #except HTTPError or URLError:
           # connected=False
           # print("network down")
        except:
            print("network down")
            connected= False
            led.set([{},'yellow','yellow','yellow',{},{},{},{},{},{},{},{},{},{},{},{},{},{}])
            #getwifi()
        else:
            connected=True
            print("up")
            led.set([{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}])
            
        time.sleep(1)
#this method, i used it in nestorestreamtext_2 for that it doesnt let the code repeat unless there is internet connection again
def testinternet():
    connected=False
    while not connected:
        try: 
            socket.setdefaulttimeout(23)
            response=  urlopen("http://www.google.com")
         
        #except HTTPError or URLError:
           # connected=False
           # print("network down")
        except:
            print("network down")
            connected= False
            led.set([{},'yellow','yellow','yellow',{},{},{},{},{},{},{},{},{},{},{},{},{},{}])
            #getwifi()
        else:
            connected=True
            print("up")
            led.set([{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}])
            
            
        time.sleep(1)
        
        
class userprofile(object):  
    def __init__(self):
            with open('/home/pi/nestore/userprofile.json') as json_file:
               data=json.load(json_file)
               self.usertoken=data['user-id']
               self.lang_id=data['lang-id']
               self.stop=0
               
    def testuserfile(self):
   
            if(not self.usertoken or not self.usertoken):
                    if (not self.lang_id):
                        lang_code="en-US"
                        print("please select ur language-id")
                        text_to_say="please sign in and make sure you select the language as well"
                        
                    elif (not self.usertoken):
                        lang_code=self.lang_id
                        
                        text_to_say="please select ur user token"
                        print(text_to_say)
                  
                        
                    try:   
                    #play audio
                            client_1 = texttospeech.TextToSpeechClient()
                           
                             #  synthesis_input = texttospeech.types.SynthesisInput(text=apiresp)
                      
            #print(rt.text)    
                            audio_config_1 = texttospeech.types.AudioConfig(
                                       audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16,sample_rate_hertz= 99000)    
                            voice = texttospeech.types.VoiceSelectionParams(
                                                language_code=lang_code,
                                           ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)  
                            synthesis_input = texttospeech.types.SynthesisInput(text=text_to_say)

                            response_1 = client_1.synthesize_speech(synthesis_input, voice, audio_config_1)
                                  
                            wav= wave.open('recording.wav', 'w')
                                                        #ATE1=wav.getframerate()
                            wav.setnchannels(2)
                            wav.setsampwidth(2)
                            wav.setframerate(44100)
                                                        #av.setparams(CHANNELS,2, 44100,1,2,3)16
                            wav.writeframes(response_1.audio_content)
                            wav.close()
                            print('Audio content written to file "recording.wav"')

                            pixels.speak_nestore()
                            os.system("aplay -D hw:2,1 /home/pi/nestore/recording.wav")
                            self.stop=1
                            #return self.stop
                    except:
                        testinternet()
                        return self.lang_id, self.usertoken , self.stop   
                        
            else:
                    self.stop=0
                    return self.lang_id, self.usertoken , self.stop       
            
            
userprofile=userprofile()

