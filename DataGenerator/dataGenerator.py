import random
from datetime import datetime, timezone, timedelta
import datetime as dt

year = 2022
month = 2
day = 15
zone = 3

bytes = [246,210]
LOC = [9321,8138,8193]

# generate random time of the day
hour = 1
previousDate= -1
while hour < 24:
    min = 0
    while min < 59:
        sec = 0
        while sec < 59:
            date = dt.datetime(year, month, day, hour, min, sec,tzinfo=timezone(timedelta(hours=zone)))

            if previousDate == -1:
                dateDiff = 0
            else:
                dateDiff = date - previousDate   

            distance=random.randint(1,14)    
            print(str(date.strftime("%Y-%m-%dT%H:%M:%S%z"))+";"+str(random.choice(bytes))+";"+str(dateDiff)+";"+str(distance)+";"+str(random.choice(LOC)))
            previousDate = date
            sec = random.randint(sec+1,60)
        min = random.randint(min+1,60)
    hour = random.randint(hour+1,24)
