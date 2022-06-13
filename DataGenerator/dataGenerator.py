import random
from datetime import datetime, timezone, timedelta
import datetime as dt
import pandas as pd


def randomData(startYear=2022, startMonth=2, startDay=15, zone=3,
               numOfDays=5, minDiffBetweenDays=1, maxDiffBetweenDays=5, minDiffBetweenMins=1, maxDiffBetweenMins=10):
    fullDate = dt.datetime(startYear, startMonth, startDay, 0,
                           1, 0, tzinfo=timezone(timedelta(hours=zone)))

    bytes = [246, 210]
    LAC = [9321, 8138, 8193]

    df = pd.DataFrame()
    # Initialize empty dataframe
    for column in ["load_date", "time", "bytes", "last_location", "travel_distance", "LAC"]:
        df[column] = ""

    # generate random time of the day
 
    previousDate = -1

    for i in range(numOfDays):
        fullDate = dt.datetime(fullDate.year, fullDate.month, fullDate.day, 0,
                               1, 0, tzinfo=timezone(timedelta(hours=zone)))

        maxTime = dt.datetime(fullDate.year, fullDate.month, fullDate.day, 23,
                              59, 59, tzinfo=timezone(timedelta(hours=zone)))
        # Iterate time
        while(True):
            if previousDate == -1:
                dateDiff = 1  # If set to 0, the program will crash due to DivisionByZero exception
            else:
                dateDiff = int((fullDate - previousDate).total_seconds())

            distance = random.randint(1, 14)

            df = pd.concat([df, pd.DataFrame.from_records([{'load_date': fullDate.date(),
                                                            'time': fullDate.minute + fullDate.hour * 60,
                                                            'bytes': random.choice(bytes),
                                                            'last_location': dateDiff,
                                                            'travel_distance': distance,
                                                            'LAC': random.choice(LAC), }])], ignore_index=True)
            previousDate = fullDate

            tempFullDate = fullDate + timedelta(minutes=random.randint(
                minDiffBetweenMins, maxDiffBetweenMins))
            if(tempFullDate < maxTime):
                fullDate = tempFullDate
            else:
                break

           
        fullDate = fullDate + \
            timedelta(days=random.randint(
                minDiffBetweenDays, maxDiffBetweenDays))

    return df