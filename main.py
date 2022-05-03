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

df = dataGenerator.randomData()

anomalyDetector = anomalyDetection.AnomalyDetector(df)
outlier_indexes = anomalyDetector.findAnomalies()
anomalyDetector.drawAnomalies(outlier_indexes)

######