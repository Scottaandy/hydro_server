from gpiozero import *
import functools
import time
import syslog

userled = LED(10)       # user led

pss33 = Button(9)       # power supply supervisor 3.3v
pss50 = Button(11)      # power supply supervisor 5.0v

pump1 = LED(23)        # relay 0
fan = LED(24)        # relay 1
pump2 = LED(25)        # relay 0

trmtr0 = LED(17)        # thermometer 0
trmtr1 = LED(4)        # thermometer 1

hmdty0 = LED(27)        # humidity 0
hmdty1 = LED(22)        # humidity 1

# Decorator to apply to jobs to get generic logging
# ------------------------------------------------------------------------
def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        syslog.syslog(syslog.LOG_INFO, 'Job "%s" running ' % (func.__name__))
        print('Job "%s" running ' % (func.__name__))
        
        result = func(*args, **kwargs)

        syslog.syslog(syslog.LOG_INFO, 'Job "%s" completed ' % (func.__name__))
        print('Job "%s" running ' % (func.__name__))
        return result
    return wrapper

class BioControle:
    def __init__(self):
        if pss33.is_pressed == 0:   # check if +3.3v good
            syslog.syslog(syslog.LOG_INFO, 'Testing +3.3V......OK')
            print('Testing +3.3V......OK')
        else:
            syslog.syslog(syslog.ERROR, 'Testing +3.3V......DEFAULT')
            print('Testing +3.3V......DEFAULT')

        if pss50.is_pressed == 0:   # check if +5.0v good
            syslog.syslog(syslog.LOG_INFO, 'Testing +3.3V......OK')
            print('Testing +5.0V......OK')
        else:
            syslog.syslog(syslog.ERROR, 'Testing +3.3V......DEFAULT')
            print('Testing +5.0V......DEFAULT')

    # ------------------------------------------------------------------------
    @with_logging
    def run_pump(self, run_time):
        userled.on()
        pump1.on()
        time.sleep(run_time)
        pump1.off()
        userled.off()

    # ------------------------------------------------------------------------
    @with_logging
    def run_circulate(self, run_time):
        userled.on()
        pump2.on()
        time.sleep(run_time)
        pump2.off()
        userled.off()

    # ------------------------------------------------------------------------
    @with_logging
    def run_fan(self, run_time):
        fan.on()
        time.sleep(run_time)
        fan.off()

        