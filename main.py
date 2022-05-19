# TO DO: Read in an array of data and use the below algorithm to check for anomalies

# TO DO: Using "dataGenerator.py" create an array of data that would simulate an attack
# And feed it to the below algorithm


#####
# # Libraries
from sklearn.datasets import make_blobs
from numpy import quantile, random, where
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import dash
import random
import pandas as pd
import numpy as np
#####

#####
# # Additional files
import AnomalyDetection.anomalyDetection as anomalyDetection
from DataGenerator import dataGenerator
#####


#####
# # Main code

# app = dash.Dash(__name__)

numOfDaysForData = 20
numOfDaysForAnomaliesData = 2

data = dataGenerator.randomData(startYear=2022, startMonth=5, startDay=10, zone=3,
                                     minDiffBetweenDays=1, maxDiffBetweenDays=10, 
                                     minDiffBetweenMins=1, maxDiffBetweenMins=480, 
                                     numOfDays=numOfDaysForData)
                                    
anomalyDetector = anomalyDetection.AnomalyDetector(data)

# anomalyDetector = anomalyDetection.AnomalyDetector(df, app)
# anomalyDetector.plotAnomaliesLive()

# # Draws a graph of anomalies for all columns
anomaly_indexes = anomalyDetector.getAnomalyIndexes()
anomalyDetector.drawAnomaliesAllColumns(anomaly_indexes)

# Goes further in as to why each data point is an anomaly
anomalyDetector.identifyAnomalies()

######

# if __name__ == '__main__':
#   app.run_server(host="127.0.0.1", port=8080, debug=True)
