#import paho.mqtt.client as mqtt
import json
from everloop2 import pixels
from checkTangData import userprofile




def on_connect( client, userdata, flags, rc):
                    print("Connected with result code " + str(rc))
                    client.subscribe("topic/test")


def on_message(client, userdata, msg):
                    if msg.payload.decode() == "notification":
                        print("Yes!")
                        pixels.notification_nestore()
                        notification=1
                        saveNotification("emotion", notification)
                    elif msg.payload.decode() == "changelanguage":
                        print("change language!")

                        changeLanguageNotification()



                        #client.disconnect()
                        
                        
def saveNotification(notif_name, notification):

    notif={notif_name : notification}
    with open("/home/pi/nestore/notification.json", "w") as jsonFile:
           json.dump(notif, jsonFile)

def changeLanguageNotification():
    usertoken= userprofile.usertoken
    print(usertoken)
    headers_iam = {"Authorization": usertoken}
    URL="https://api.nestore-coach.eu/dev/hesso/coach/profile"

    try:
            print(1)              
            req = requests.get(URL, headers=headers_iam)
            print(2)
            response= req.json()
            print(3)
            print(response['lang'])
            # save it to userprofile.json



    except:
            print("eroor")

if __name__ == '__main__':

    client = mqtt.Client()
    client.connect("172.20.10.3", 1883, 60)

    client.on_connect = on_connect
    client.on_message = on_message

    client.loop_forever()

