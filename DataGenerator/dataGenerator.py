import random
from datetime import datetime, timezone, timedelta
import datetime as dt
import pandas as pd

def randomData():
    year = 2022
    month = 2
    day = 15
    zone = 3

    bytes = [246,210]
    LAC = [9321,8138,8193]

    df = pd.DataFrame()
    # Initialize empty dataframe
    for column in [ "time", "bytes", "last_location", "travel_distance", "LAC" ]:
        df[column] = ""

    # generate random time of the day
    hour = 1
    previousDate = -1

    while hour < 24:
        min = 0
        while min < 59:
            sec = 0
            while sec < 59:
                date = dt.datetime(year, month, day, hour, min, sec,tzinfo=timezone(timedelta(hours=zone)))

                if previousDate == -1:
                    dateDiff = date - date
                else:
                    dateDiff = date - previousDate   

                distance=random.randint(1,14)

                # If possible we'll group data by the minute (look at "time" column).
                df = df.append({'time' : date.minute + hour * 60, 
                                'bytes' : random.choice(bytes), 
                                'last_location' : int(dateDiff.total_seconds()),  
                                'travel_distance' : distance,  
                                'LAC' : random.choice(LAC), }, ignore_index = True)

                #print(date.strftime("%Y-%m-%dT%H:%M:%S%z"))+";"+str(random.choice(bytes))+";"+str(dateDiff)+";"+str(distance)+";"+str(random.choice(LAC)))
                previousDate = date
                sec = random.randint(sec+1,60)
            min = random.randint(min+1,60)
        hour = random.randint(hour+1,24)

    return df
