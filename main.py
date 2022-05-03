# TO DO: Read in an array of data and use the below algorithm to check for anomalies

# TO DO: Using "dataGenerator.py" create an array of data that would simulate an attack
# And feed it to the below algorithm


##### Libraries
from sklearn.datasets import make_blobs
from numpy import quantile, random, where
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

##### Additional files
from AnomalyDetection import anomalyDetection


###### Sample input, change later.
random.seed(3)
X, _ = make_blobs(n_samples=300, centers=1, cluster_std=.3, center_box=(20, 5))
print(X)
anomalyDetection.drawAnomalyGraph(X, _)
######