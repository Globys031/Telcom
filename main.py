# TO DO: Read in an array of data and use the below algorithm to check for anomalies

# TO DO: Using "dataGenerator.py" create an array of data that would simulate an attack
# And feed it to the below algorithm


#####
# # Libraries
from sklearn.datasets import make_blobs
from numpy import quantile, random, where
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
#####

#####
# # Additional files
from AnomalyDetection import anomalyDetection
from DataGenerator import dataGenerator
#####


#####
# # Main code

df = dataGenerator.randomData(startYear=2022, startMonth=5, startDay=10, zone=3,
               numOfDaysToGenerateData=10, minDifferenceBetweenDays=1, maxDifferenceBetweenDays=5)

anomalyDetector = anomalyDetection.AnomalyDetector(df)

# # Draws a graph of anomalies for all columns
# TO DO: get rid of the error when these two are uncommented
#anomaly_indexes = anomalyDetector.getAnomalyIndexes()
#anomalyDetector.drawAnomaliesAllColumns(anomaly_indexes)

# Goes further in as to why each data point is an anomaly
anomalyDetector.identifyAnomalies()

######