from gpiozero import *
from time import *

# IOs

userled = LED(10)       # user led

pss33 = Button(9)       # power supply supervisor 3.3v
pss50 = Button(11)      # power supply supervisor 5.0v

pump = LED(23)        # relay 0
fan = LED(24)        # relay 1
circ = LED(25)        # relay 2
other = LED(26)

trmtr0 = LED(17)        # thermometer 0
trmtr1 = LED(4)        # thermometer 1

hmdty0 = LED(27)        # humidity 0
hmdty1 = LED(22)        # humidity 1

def test_power():
    print("Testing +3.3V......", end = "")
    if pss33.is_pressed == 0:   # check if +3.3v good
        print("OK")
    else:
        print("DEFAULT")

    print("Testing +5.0V......", end = "")
    if pss50.is_pressed == 0:   # check if +5.0v good
        print("OK")
    else:
        print("DEFAULT")
        
def activate_relay(relay, num_seconds):
    print('Relay ON for {0}'.format(num_seconds))
    relay.on()
    sleep(num_seconds)
    relay.off()
    
# MAIN
test_power()
userled.on()
activate_relay(pump, 5)
activate_relay(circ, 5)
activate_relay(fan, 5)
other.off()

#activate_relay(relay1, 60)
userled.off()

