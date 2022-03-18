from sklearn.datasets import make_blobs
from numpy import quantile, random, where
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt


def drawAnomalyGraph(X, _):
  # https://machinelearningmastery.com/anomaly-detection-with-isolation-forest-and-kernel-density-estimation/
  plt.scatter(X[:, 0], X[:, 1], marker="o", c=_, s=25, edgecolor="k")

  IF = IsolationForest(n_estimators=100, contamination=.03)
  predictions = IF.fit_predict(X)

  # -1 is for outliers and 1 for regular data 
  outlier_index = where(predictions==-1)
  values = X[outlier_index]
  plt.scatter(X[:,0], X[:,1])
  plt.scatter(values[:,0], values[:,1], color='y')
  plt.show()