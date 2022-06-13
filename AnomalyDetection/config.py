import dash

# This file contains global variables used throughout the code

# dfs will contain multiple anomaly dataframes
# for each of the columns. The dataframes inside dfs will later be 
# appended to by dataGenerator.py
dfs = []
dates = []
bool_array = []
actuals = []
anomaly_points = []

df_orig = 0
metric_name = "No metric name yet"

app = dash.Dash(__name__)

# The longer it takes for the callback function in anomalyIllustrator calculate
# The more likely the graphs will become empty. To avoid that, the calculations
# that can be done globally - will be done here