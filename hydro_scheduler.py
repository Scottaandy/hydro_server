from gpiozero import *
import functools
import threading
import time
import schedule
import atexit

# IOs
# ------------------------------------------------------------------------
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

# ------------------------------------------------------------------------
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
        
# Decorator to apply to jobs to get generic logging
# ------------------------------------------------------------------------
def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Job "%s" running' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper
       
# ------------------------------------------------------------------------
@with_logging
def run_pump(run_time):
    userled.on()
    pump1.on()
    time.sleep(run_time)
    pump1.off()
    userled.off()
    display_jobs()

# ------------------------------------------------------------------------
@with_logging
def run_circulatet(run_time):
    userled.on()
    pump2.on()
    time.sleep(run_time)
    pump2.off()
    userled.off()
    display_jobs()

# ------------------------------------------------------------------------
@with_logging
def run_fan(run_time):
    fan.on()
    time.sleep(run_time)
    fan.off()
    display_jobs()

# ------------------------------------------------------------------------
def display_jobs():
    print('------------------------------------------------------------------')
    for job in schedule.jobs:
        print(job)
    print('------------------------------------------------------------------')
    print()
    
# ------------------------------------------------------------------------
def run_threaded(job_func, run_time):
    print('running thread')
    job_thread = threading.Thread(target=job_func, args=[run_time])
    job_thread.start()

# ------------------------------------------------------------------------
@atexit.register
def cleanup():
    print('Cleaning up before exit')
    pump.off()
    fan.off()
    userled.off()

        
# MAIN
# ------------------------------------------------------------------------
def main():
    test_power()

    pump_duration = 300
    fan_duration = 200
    circ_duration = 1800

    # Pump schedule
    schedule.every().day.at("08:00").do(run_threaded, run_pump, run_time=pump_duration)
    schedule.every().day.at("13:00").do(run_threaded, run_pump, run_time=pump_duration)
    schedule.every().day.at("18:00").do(run_threaded, run_pump, run_time=pump_duration)
    # Fan schedule
    schedule.every(2).hours.do(run_threaded, run_fan, run_time=fan_duration)
    # Circulation pump schedule
    schedule.every().day.at("07:45").do(run_threaded, run_pump, run_time=circ_duration)
    schedule.every().day.at("12:45").do(run_threaded, run_pump, run_time=circ_duration)
    schedule.every().day.at("17:45").do(run_threaded, run_pump, run_time=circ_duration)
    
    # Job display schedule
    #schedule.every(15).minutes.do(display_jobs)

    display_jobs()

    while(1):
        try:
            schedule.run_pending()
            time.sleep(10)
            userled.toggle()
            
        except (KeyboardInterrupt, SystemExit):
            cleanup()
            exit()


# ------------------------------------------------------------------------
main()
print("exit")