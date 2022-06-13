#####
# # Libraries
from sklearn.datasets import make_blobs
from numpy import quantile, random, where
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import dash
import warnings
import numpy as np
#####

#####
# # Additional files
from DataGenerator import dataGenerator
from AnomalyDetection import anomalyDetection, anomalyIllustrator, config
#####

if __name__ == '__main__':
	live_mode = True

	# config.df is a global variables that will is necessary to draw data live
	config.df = dataGenerator.randomData(startYear=2022, startMonth=5, startDay=10, zone=3,
								numOfDays=10, minDiffBetweenDays=1, maxDiffBetweenDays=5)
	# config.df will have some of its data changed to determine anomalies, but we still
	# need the original unaltered data
	config.df_orig = config.df

	model = anomalyDetection.getModel()
	warnings.filterwarnings('ignore')

	# Currently this code will append the initial data arrays. 
	# Further down the line it would be best if to each of the the dataframes inside config.dfs
	# (and other variables here) you would append additional data to the very end.
	# They're global configs because the callback function for anomalyIllustrator can't be allowed
	# to take too long to calculate
	for i in range(1,len(config.df.columns)):
		config.dfs.append(anomalyDetection.identifyAnomaliesForColumn(model, config.df_orig, i))
		config.metric_name = config.df_orig.columns[i]
		
		config.dates.append(config.dfs[i - 1]['load_date'])

		# identify anomaly points and create an array of anomaly's values for plot
		config.bool_array.append((abs(config.dfs[i - 1]['anomaly']) > 0))
		config.actuals.append(config.dfs[i - 1]["actuals"][-len(config.bool_array[i - 1]):])
		# All of the non-anomaly values are going to be NaN
		config.anomaly_points.append(config.bool_array[i - 1] * config.actuals[i - 1])
		config.anomaly_points[i - 1][config.anomaly_points[i - 1] == 0] = np.nan

	if live_mode == True:
		anomalyIllustrator.plotAnomaliesLive()
		config.app.run_server(host="127.0.0.1", port=8080, debug=True)
	else:
		#########################
		# # # Gets what data is classified as anomalies depending on all columns
		anomaly_indexes = anomalyDetection.getAnomalyIndexes(config.df_orig)
		# # # Draws a graph of anomalies for all columns
		anomalyIllustrator.drawAnomaliesAllColumns(anomaly_indexes)

		########## This part is used to identify anomalies for each column
		# "load_date" is only used for graphical purposes so it needs to be skipped
		for i in range(1,len(config.df_orig.columns)-1):
		  # Gets new dataframe where "anomaly" column only judges one of the attributes
		  anomalyIllustrator.plotAnomalies(config.dfs[i - 1], config.df_orig.columns[i])
		###########
