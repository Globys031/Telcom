from sklearn.datasets import make_blobs
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

from numpy import quantile, random, where

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class AnomalyDetector:
  def __init__(self, learning_data):
    self.learning_data = learning_data

  def printInput(self):
    print(self.learning_data)

  # Currently there's no contamination as there's no attack data examples. But you can't have
  # contamination = 0. So for now 0.01 will suffice.
  # TO DO: gather (or generate yourself) attack data. We'll later use the algorithm to check if
  # that data appears as anomalies
  def findAnomalies(self):
    # We're going to use all columns for anomaly detection
    # The only column that might not be of importance is "time", but for now we'll leave it as is.
    # contamination - percentage of outlier points in the data
    model=IsolationForest(n_estimators=100, max_samples='auto', contamination=0.01,
                          max_features=1.0, bootstrap=False, n_jobs=-1, random_state=42, verbose=0)
    # Fits the models and makes predictions on whether there's outliers
    model.fit(self.learning_data.values)
    self.learning_data['anomaly'] = model.predict(self.learning_data.values)
    outliers = self.learning_data.loc[self.learning_data['anomaly'] == -1]
    # Gets the indexes of data that are anomalies
    outlier_indexes = list(outliers.index)

    return outlier_indexes


  def drawAnomalies(self, outlier_indexes):
    # PCA is primarily used for dimensionality reduction (basically allows to display multiple columns in 2D)
    pca = PCA(2)
    pca.fit(self.learning_data.values)

    # It seems to be calculated differently every time
    transformed_data = pd.DataFrame(pca.transform(self.learning_data.values))

    plt.title("IsolationForest")

    b1 = plt.scatter(transformed_data[0], transformed_data[1], c='green', s=20,label="normal points")
    b1 = plt.scatter(transformed_data.iloc[outlier_indexes, 0], transformed_data.iloc[outlier_indexes, 1], c='red',s=20,label="predicted outliers")
    
    plt.legend(loc="upper right")
    plt.show()
