from datetime import datetime
import functools

date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
print('%s: Job "%s" running' % (date_time, "job x"))
