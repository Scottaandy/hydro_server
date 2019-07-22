import threading
import time
from datetime import datetime
import schedule
import atexit
import SocketServer
import BioControle
import syslog

# ------------------------------------------------------------------------
def display_jobs():
    print('------------------------------------------------------------------')
    for job in schedule.jobs:
        print(job)
    print('------------------------------------------------------------------')
    print()
    
# ------------------------------------------------------------------------
def run_threaded(job_func, run_time):
    job_thread = threading.Thread(target=job_func, args=[run_time])
    job_thread.start()

# ------------------------------------------------------------------------
@atexit.register
def cleanup():
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    syslog.syslog(syslog.LOG_INFO, '%s: Cleaning up before exit ' % (date_time))
    print('%s: Cleaning up before exit ' % (date_time))
    pump.off()
    circ.off()
    fan.off()
    userled.off()

def process_request(data, server, client_sock, bio):
    #print(data[0])
    s = data[0].decode()
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    syslog.syslog(syslog.LOG_INFO, '%s: Received Message: << %s >> ' % (date_time, s))
    print('%s: Received Message: << %s >> ' % (date_time, s))
    
    if 'GET /?circ=' in s:
        result = int(s[s.find('circ=')+5:s.find(' HTTP')],10)
        server.send_response(client_sock, "Circulating for {} seconds".format(result));
        run_threaded(bio.run_circulate, result)
        #bio.run_circulate(result)
    if 'GET /?pump=' in s:
        result = int(s[s.find('pump=')+5:s.find(' HTTP')])
        server.send_response(client_sock, "Pumping for {} seconds".format(result));
        run_threaded(bio.run_pump, result)
        #bio.run_pump(result)
    if 'GET /?fan=' in s:
        result = int(s[s.find('fan=')+4:s.find(' HTTP')])
        server.send_response(client_sock, "Fanning for {} seconds".format(result));
        run_threaded(bio.run_fan, result)
        #bio.run_fan(result)
    if 'GET /?status' in s:
        status = "<html><head></head><body>"
        status = status + "<h2>Current Schedule</h2><hr><ul>"
        for job in schedule.jobs:
            status = status + "<li>" + str(job) + "</li>\n"
        status = status + "</ul></body>"
        server.send_response(client_sock, status)
        
# MAIN
# ------------------------------------------------------------------------
def main():
    server = SocketServer.SocketServer()
    bio = BioControle.BioControle()
    
    pump_duration = 300
    fan_duration = 200
    circ_duration = 1800

    # Pump schedule
    schedule.every().day.at("08:00").do(run_threaded, bio.run_pump, run_time=pump_duration)
    schedule.every().day.at("13:00").do(run_threaded, bio.run_pump, run_time=pump_duration)
    schedule.every().day.at("18:00").do(run_threaded, bio.run_pump, run_time=pump_duration)
    #schedule.every().day.at("19:25").do(run_threaded, bio.run_pump, run_time=pump_duration)
    # Fan schedule
    schedule.every(2).hours.do(run_threaded, bio.run_fan, run_time=fan_duration)
    # Circulation pump schedule
    schedule.every().day.at("07:45").do(run_threaded, bio.run_circulate, run_time=circ_duration)
    schedule.every().day.at("12:45").do(run_threaded, bio.run_circulate, run_time=circ_duration)
    schedule.every().day.at("17:45").do(run_threaded, bio.run_circulate, run_time=circ_duration)
    
    # Job display schedule
    #schedule.every(15).minutes.do(display_jobs)
    display_jobs()
    
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    syslog.syslog('%s: Server Ready ' % (date_time))
    print('%s: Server Ready ' % (date_time))

    sleepTimer = 10;
    while True:

        try:
            schedule.run_pending()
            
            try:
                (data, client_sock) = server.check_select()
                if data:
                    process_request(data, server, client_sock, bio)
                    server.close_client(client_sock)

            except:
                pass
                    
            time.sleep(sleepTimer)
            BioControle.userled.toggle()
            
        except (KeyboardInterrupt, SystemExit):
            cleanup()
            exit()


# ------------------------------------------------------------------------
main()
print("exit")