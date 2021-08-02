
from __future__ import division
import requests

import re
import sys
import json
import os

from everloop2 import pixels

import time

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

import checkTangData
from checkTangData import userprofile
from mqttclient import saveNotification
import random
random.seed( 30 )
from google.cloud import texttospeech
import wave
import signal
def signal_handler():
    raise IOError("kill")
signal.signal(signal.SIGINT, signal_handler)

import board
import digitalio
import busio
import adafruit_lis3dh

i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)  # Set this to the correct pin for the interrupt!
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

URL="https://api.nestore-coach.eu/dev/hesso/coach/chatbot/tangible/message"
os.environ[
   "GOOGLE_APPLICATION_CREDENTIALS"] = "/home/pi/nestore/credentials.json"
lang_id, usertoken, stop = userprofile.testuserfile()


# Audio recording parameters
RATE = 16000
CHUNK = 1024
# CHUNK = int(RATE / 10*3 )  # 100ms
RECORD_SECONDS = 5000
CHANNELS = 2
client = speech.SpeechClient()
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code=lang_id,
    enable_word_time_offsets=True,
    speech_contexts=[speech.types.SpeechContext(
        phrases=['nutritional', 'yes', 'no', 'physical', 'feelings', 'emotions', 'home', 'nestore'],
    )],

)
streaming_config = types.StreamingRecognitionConfig(
    config=config,
    interim_results=True,
    single_utterance=True)
client_1 = texttospeech.TextToSpeechClient()

#  synthesis_input = texttospeech.types.SynthesisInput(text=apiresp)
voice = texttospeech.types.VoiceSelectionParams(
    language_code=lang_id,
    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
# print(rt.text)
audio_config_1 = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.LINEAR16, sample_rate_hertz=99000)

# timefinished=0
# Speech to text
def get_current_time():
    return int(round(time.time() * 1000))


def duration_to_sec(duration):
    return duration.seconds + (duration.nanos / float(1e9))


class Error(Exception):
    pass


class accelerometergoesoff(Error):
    pass


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data

        self._buff = queue.Queue()
        self.closed = True
        self.start_time = get_current_time()
        self.timefinished = 0
        self.stop = stop

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""

        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            print(get_current_time() - self.start_time)
            if get_current_time() - self.start_time > RECORD_SECONDS:
                self.start_time = get_current_time()

                self.timefinished = 1

                break
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)

                    if chunk is None:
                        return
                    data.append(chunk)

                except queue.Empty:
                    break

            yield b''.join(data)

    def listen(self):




               
                pixels.listen_nestore()
                isresponse = False
                with MicrophoneStream(RATE, CHUNK) as stream:
                   

                        audio_generator = stream.generator()
                        print("say something")



                        time.sleep(0.1)
           
                        try:
                                requests_1 = (types.StreamingRecognizeRequest(audio_content=content)
                                              for content in audio_generator)


                                print("1 a")
                                responses = client.streaming_recognize(streaming_config, requests_1)
                                print("2 a")

                                for response in responses:

                                    for result in response.results:
                                        # print("question"+result.alternatives[0].transcript)

                                        if (result.is_final == True):
                                            stream.__exit__(None, None, None)
                                            question = result.alternatives[0].transcript
                                            isresponse = True
                                            return question

                                if (stream.timefinished == 1 and not isresponse):
                                    self.stop = 1
                                    question = "goodbye"  #to change the sentence 
                                    print("stream empty close")
                                    return question
                        except:
                            print("eror")
                            self.stop=1
                            pixels.off_nestore()


    def think(self, question):


                                         
                            pixels.think_nestore()
                           # print("question " + str(question))
                            headers = {"Authorization": usertoken}
                            try:
                            # checkTangData.testuserprofile(usertoken,lang_id)
                                    req = requests.post(URL,
                                                        json={"text": question}, headers=headers)

                                    j = json.loads(req.text)

                                    apiresp = j["text"]
                                  
                                    if 'discussionEnd' in j:
                                        if j["discussionEnd"] == 1:
                                            print("stop")
                                            self.stop = 1

                                    synthesis_input = texttospeech.types.SynthesisInput(text=apiresp)

                                    response_1 = client_1.synthesize_speech(synthesis_input, voice, audio_config_1)

                                    wav = wave.open('/home/pi/nestore/recording.wav', 'w')
                               
                                    wav.setnchannels(CHANNELS)
                                    wav.setsampwidth(2)
                                    wav.setframerate(44100)
                           
                                    wav.writeframes(response_1.audio_content)
                                    wav.close()
                                    print('Audio content written to file "recording.wav"')
                            except:
                                print("Error")
                                self.stop=1
                                pixels.off_nestore() ###play sound that there is no internet 

                       
    def speak(self):
                            pixels.speak_nestore()
                            os.system("aplay -D hw:2,1 /home/pi/nestore/recording.wav")

    def conversation(self):
         self.stop = 0
       
         print("notification", self.getnotification())
         self.notificationConversation(self.getnotification())
         
         
         
         
         while not self.stop:
            #with MicrophoneStream(RATE, CHUNK) as conv:

                question=self.listen()
                self.think(question)
                self.speak()
                self.accelerometer()

         pixels.off_nestore()

    def notificationConversation(self, Isnotification):
        if(Isnotification==1):
            print("i am here")
            saveNotification("emotion", 0) ###does not work to check
            question= "it is the end of the day"
            self.think(question)
            self.speak()
            
    def getnotification(self):
        with open('/home/pi/nestore/notification.json') as jsonfile:
             data= json.load(jsonfile)
             Isnotification=data['emotion']
             return Isnotification



    def accelerometer(self):
        
          if(lis3dh.acceleration[2]>8 and lis3dh.acceleration[2]<11): 
              self.stop=1
              pixels.off_nestore()
              print("i am checed")
nestoreconv = MicrophoneStream(RATE, CHUNK)

if __name__ == '__main__':

    nestoreconv.conversation()




