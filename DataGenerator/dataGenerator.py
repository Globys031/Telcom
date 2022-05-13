import random
from datetime import datetime, timezone, timedelta
import datetime as dt
import pandas as pd


def randomData(startYear=2022, startMonth=2, startDay=15, zone=3,
               numOfDaysToGenerateData=5, minDifferenceBetweenDays=1, maxDifferenceBetweenDays=5):

    date = dt.date(startYear, startMonth, startDay)

    bytes = [246, 210]
    LAC = [9321, 8138, 8193]

    df = pd.DataFrame()
    # Initialize empty dataframe
    for column in ["load_date", "time", "bytes", "last_location", "travel_distance", "LAC"]:
        df[column] = ""

    # generate random time of the day
    hour = 1
    previousDate = -1

    # Generate date
    for i in range(numOfDaysToGenerateData):
        # generate random time of the day
        hour = 1
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
                        dateDiff = int(
                            (fullDate - previousDate).total_seconds())

                    distance = random.randint(1, 14)

                    # If possible we'll group data by the minute (look at "time" column).
                    df = pd.concat([df, pd.DataFrame.from_records([{'load_date': date,
                                    'time': min + hour * 60,
                                                                    'bytes': random.choice(bytes),
                                                                    'last_location': dateDiff,
                                                                    'travel_distance': distance,
                                                                    'LAC': random.choice(LAC), }])], ignore_index=True)

                    # print(str(fullDate.strftime("%Y-%m-%dT%H:%M:%S%z"))+";"+str(random.choice(bytes)
                    # )+";"+str(dateDiff)+";"+str(distance)+";"+str(random.choice(LOC)))
                    previousDate = fullDate
                    sec = random.randint(sec+1, 60)
                min = random.randint(min+1, 60)
            hour = random.randint(hour+1, 24)
        date = date + \
            timedelta(days=random.randint(
                minDifferenceBetweenDays, maxDifferenceBetweenDays))
    return df
