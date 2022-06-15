import random
from datetime import datetime, timezone, timedelta
import datetime as dt
import pandas as pd


def randomData(startYear=2022, startMonth=2, startDay=15, zone=3,
               numOfDays=5, minDiffBetweenDays=1, maxDiffBetweenDays=5, minDiffBetweenMins=1, maxDiffBetweenMins=10):
    fullDate = dt.datetime(startYear, startMonth, startDay, 0,
                           1, 0, tzinfo=timezone(timedelta(hours=zone)))

    sender = [310170845466094, 470040123456789, 502130123456789, 460001357924680, 520031234567890, 313460000000001]
    receiver = [310170845466994, 470040123456989, 502130123456989, 460001357924980, 520031234567990, 313460000000901]

    df = pd.DataFrame()
    # Initialize empty dataframe
    for column in ["load_date", "time", "sender", "receiver"]:
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
            df = pd.concat([df, pd.DataFrame.from_records([{'load_date': fullDate.date(),
                                                            'time': fullDate.minute + fullDate.hour * 60,
                                                            'sender': random.choice(sender),
                                                            'receiver': random.choice(receiver),
                                                            }])], ignore_index=True)
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