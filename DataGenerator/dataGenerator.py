import random
from datetime import datetime, timezone, timedelta
import datetime as dt

startYear = 2022
startMonth = 2
startDay = 15
zone = 3

numOfDaysToGenerateData = 20
generateRandomDate = False;

date = dt.date(startYear, startMonth, startDay)

bytes = [246, 210]
LOC = [9321, 8138, 8193]

# Generate date
for i in range(numOfDaysToGenerateData):
    # generate random time of the day
    hour = 1
    previousDate = -1
    while hour < 24:
        min = 0
        while min < 59:
            sec = 0
            while sec < 59:
                fullDate = dt.datetime(date.year, date.month, date.day,
                                       hour, min, sec, tzinfo=timezone(timedelta(hours=zone)))

                if previousDate == -1:
                    dateDiff = 0
                else:
                    dateDiff = fullDate - previousDate

                distance = random.randint(1, 14)
                print(str(fullDate.strftime("%Y-%m-%dT%H:%M:%S%z"))+";"+str(random.choice(bytes)
                                                                            )+";"+str(dateDiff)+";"+str(distance)+";"+str(random.choice(LOC)))
                previousDate = fullDate
                sec = random.randint(sec+1, 60)
            min = random.randint(min+1, 60)
        hour = random.randint(hour+1, 24)
    date = date + timedelta(days=1)
