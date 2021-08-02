#!/usr/bin/python3.5
#from pijuice import PiJuice # Import pijuice module
#pijuice = PiJuice(1, 0x14) # Instantiate PiJuice interface object
#print (pijuice.status.GetStatus()) # Read PiJuice status.
#!/usr/bin/python3
from pijuice import PiJuice # Import pijuice module

 # Instantiate PiJuice interface object
#print (pijuice.status.GetStatus()) # Read PiJuice status.
#print (pijuice.status.GetChargeLevel()['data'])
#chargelevel=pijuice.status.GetChargeLevel()['data']
from everloop2 import pixels
def getchargelevel():
    pijuice = PiJuice(1, 0x14)
    chargelevel=pijuice.status.GetChargeLevel()['data']
   ##### print (pijuice.status.GetStatus()['data']['battery'])
    batterystatus= pijuice.status.GetStatus()['data']['battery']  # charging from in if it is charging and normal if its not charging. 
    print (pijuice.status.GetChargeLevel()['data'])
    if( batterystatus== 'CHARGING_FROM_IN'):
        pixels.charging()
    if (chargelevel < 40):
        pixels.lowcharge()
    elif chargelevel > 40 and chargelevel < 90:
        pixels.mediumcharge()
    elif chargelevel > 90:
        pixels.highcharge()


#if __name__ == '__main__':
 #      getchargelevel()


