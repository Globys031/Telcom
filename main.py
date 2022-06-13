#####
# # Libraries
from sklearn.datasets import make_blobs
from numpy import quantile, random, where
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import dash
import warnings
#####

#####
# # Additional files
from DataGenerator import dataGenerator
from AnomalyDetection import anomalyDetection, anomalyIllustrator, config
#####

# config.df is a global variables that will is necessary to draw data live
config.df = dataGenerator.randomData(startYear=2022, startMonth=5, startDay=10, zone=3,
               numOfDays=10, minDiffBetweenDays=1, maxDiffBetweenDays=5)
# config.df will have some of its data changed to determine anomalies, but we still
# need the original unaltered data
df_orig = config.df

model = anomalyDetection.getModel()
warnings.filterwarnings('ignore')

#########################
# # # # Gets what data is classified as anomalies depending on all columns
# anomaly_indexes = anomalyDetection.getAnomalyIndexes(config.df)
# # # # Draws a graph of anomalies for all columns
# anomalyIllustrator.drawAnomaliesAllColumns(anomaly_indexes)

# for i in range(1,len(config.df.columns)-1):
i = 1
config.df = anomalyDetection.identifyAnomaliesForColumn(model, df_orig, i)
config.metric_name = df_orig.columns[i]
anomalyIllustrator.plotAnomaliesLive()
#########################


# ########## This part is used to identify anomalies for each column
# # "load_date" is only used for graphical purposes so it needs to be skipped
# for i in range(1,len(config.df.columns)-1):
#   # Gets new dataframe where "anomaly" column only judges one of the attributes
#   df_one_column = anomalyDetection.identifyAnomaliesForColumn(model, df_orig, i)
#   anomalyIllustrator.plotAnomalies(df_one_column, df_orig.columns[i])
# ###########


if __name__ == '__main__':
  config.app.run_server(host="127.0.0.1", port=8080, debug=True)