from sklearn.datasets import make_blobs
from sklearn.ensemble import IsolationForest
from sklearn.decomposition import PCA

from numpy import quantile, random, where
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from plotly.offline import download_plotlyjs, init_notebook_mode, plot
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly.graph_objs as go
from collections import deque

# Contains global variables used throughout the program
from AnomalyDetection import config, anomalyDetection

###########
# The "getAnomalyIndexes" and "drawAnomaliesAllColumns" display anomalies based on all columns
# The rest of the code goes by each column and further defines why each column's data
# can be considered an anomaly.
###########

def drawAnomaliesAllColumns(outlier_indexes):
  # PCA is primarily used for dimensionality reduction (basically allows to display multiple columns in 2D)
  pca = PCA(2)
  pca.fit(config.df.iloc[:,1:].values)

  # It seems to be calculated differently every time
  transformed_data = pd.DataFrame(pca.transform(config.df.iloc[:,1:].values))

  plt.title("IsolationForest")

  b1 = plt.scatter(transformed_data[0], transformed_data[1], c='green', s=20,label="normal points")
  b1 = plt.scatter(transformed_data.iloc[outlier_indexes, 0], transformed_data.iloc[outlier_indexes, 1], c='red',s=20,label="predicted outliers")
  
  plt.legend(loc="upper right")
  plt.show()

def plotAnomalies(df, metric_name):
  dates = df['load_date']

  #identify anomaly points and create an array of anomaly's values for plot
  bool_array = (abs(df['anomaly']) > 0)
  actuals = df["actuals"][-len(bool_array):]
  # All of the non-anomaly values are going to be NaN
  anomaly_points = bool_array * actuals
  anomaly_points[anomaly_points == 0] = np.nan

  #A dictionary for conditional format table based on anomaly
  color_map = {0: "gray", 1: "yellow", 2: "red"}
  
  #Table which includes Date,Actuals(dataGenerator values),Change occured from previous point
  # https://plotly.com/python/table/
  table = go.Table(
      domain=dict(x=[0, 1],
                  y=[0, 0.55]),
      columnwidth=[5, 2, 3],
      header=dict(height=20,
                  values=[['<b>Date</b>'], ['<b>Actual Values </b>'], ['<b>% Change </b>'],
                          ],
                  font=dict(color=['rgb(45,45,45)'] * 5, size=14),
                  fill=dict(color='#d562be')), #bet issiaiskinau kad tikrai sita vieta jam nepatinka
      cells=dict(values=[df.round(3)[k].tolist() for k in ['load_date', 'actuals', 'percentage_change']],
                  line=dict(color='#506784'),
                  align=['center'] * 5,
                  font=dict(color=['rgb(40,40,40)'] * 5, size=12),
                  suffix=[None] + [''] + [''] + ['%'] + [''],
                  height=27,
                  fill=dict(color=[df['anomaly'].map(color_map)],#map based on anomaly level from dictionary
                  )
                  ))
  #Plot the actuals (datagenerator data) scatter points
  Actuals = go.Scatter(name='Actuals',
                        x=dates,
                        y=df['actuals'],
                        xaxis='x1', yaxis='y1',
                        mode='lines',
                        marker=dict(size=12,
                                    line=dict(width=1),
                                    color="blue"))
  #Highlight the anomaly points
  anomalies_map = go.Scatter(name="Anomaly",
                              showlegend=True,
                              x=dates,
                              y=anomaly_points,
                              mode='markers',
                              xaxis='x1',
                              yaxis='y1',
                              marker=dict(color="red",
                                          size=11,
                                          line=dict(
                                              color="red",
                                              width=2)))
  axis = dict(
            showline=True,
            zeroline=False,
            showgrid=True,
            mirror=True,
            ticklen=4,
            gridcolor='#ffffff',
            tickfont=dict(size=10))
  layout = dict(
            width=1000,
            height=865,
            autosize=False,
            title=metric_name,
            margin=dict(t=75),
            showlegend=True,
            xaxis1=dict(axis, **dict(domain=[0, 1], anchor='y1', showticklabels=True)),
            yaxis1=dict(axis, **dict(domain=[2 * 0.21 + 0.20, 1], anchor='x1', hoverformat='.2f')))

  fig = go.Figure(data=[table, anomalies_map, Actuals], layout=layout)

  plot(fig)

# Creates a div that's set to update every second and calls a function
# That actually plots the graph
def plotAnomaliesLive():
  config.app.layout = html.Div([
      html.Div([
          dcc.Graph(id='live-graph-1', animate=True),
          dcc.Interval(
              id='graph-update-1',
              interval=5*1000, # in miliseconds
              n_intervals=0
          ),
      ]),
      html.Div([
          dcc.Graph(id='live-graph-2', animate=True),
          dcc.Interval(
              id='graph-update-2',
              interval=5*1000, # in miliseconds
              n_intervals=0
          ),
      ]),
      html.Div([
          dcc.Graph(id='live-graph-3', animate=True),
          dcc.Interval(
              id='graph-update-3',
              interval=5*1000, # in miliseconds
              n_intervals=0
          ),
      ]),
  ])
  @config.app.callback(
      # The order in which the dependency objects are provided dictates the 
      # order of the positional arguments that are passed to the decorated callback function.
      Output(component_id='live-graph-1', component_property='figure'),
      Output(component_id='live-graph-2', component_property='figure'),
      Output(component_id='live-graph-3', component_property='figure'),
      Input(component_id='graph-update-1', component_property='n_intervals'),
  ) # '@' being used, meaning that the below method is used for callback
  ###### IMPORTANT !!!
  # If the calculations inside this function take too long, they won't be properly displayed
  # in the graph. During the time it takes to fetch all of the figures, the graphs will 
  # appear empty. Because of this reason most calculations have to be done outside this function
  def update_graph_scatter(n_intervals):
      figures = []
      i = 0
    
      for df in config.dfs:
        metric_name = config.df_orig.columns[i + 1]

        color_map = {0: "gray", 1: "yellow", 2: "red"}

        # Table which includes Date,Actuals(dataGenerator values),Change occured from previous point
        # https://plotly.com/python/table/
        table = go.Table(
            domain=dict(x=[0, 1],
                        y=[0, 0.55]),
            columnwidth=[5, 2, 3],
            header=dict(height=20,
                        values=[['<b>Date</b>'], ['<b>Actual Values </b>'], ['<b>% Change </b>'],
                                ],
                        font=dict(color=['rgb(45,45,45)'] * 5, size=14),
                        fill=dict(color='#d562be')), #bet issiaiskinau kad tikrai sita vieta jam nepatinka
            cells=dict(values=[df.round(3)[k].tolist() for k in ['load_date', 'actuals', 'percentage_change']],
                        line=dict(color='#506784'),
                        align=['center'] * 5,
                        font=dict(color=['rgb(40,40,40)'] * 5, size=12),
                        suffix=[None] + [''] + [''] + ['%'] + [''],
                        height=27,
                        fill=dict(color=[df['anomaly'].map(color_map)],#map based on anomaly level from dictionary
                        )
                        ))

        # Plot the actuals (datagenerator data) scatter points
        Actuals = go.Scatter(name='Actuals',
                            x=config.dates[i],
                            y=df['actuals'],
                            xaxis='x1', yaxis='y1',
                            mode='lines',
                            marker=dict(size=12,
                                        line=dict(width=1),
                                        color="blue"))

        #Highlight the anomaly points
        anomalies_map = go.Scatter(name="Anomaly",
                                  showlegend=True,
                                  x=config.dates[i],
                                  y=config.anomaly_points[i],
                                  mode='markers',
                                  xaxis='x1',
                                  yaxis='y1',
                                  marker=dict(color="red",
                                              size=11,
                                              line=dict(
                                                  color="red",
                                                  width=2)))

        axis = dict(
                    showline=True,
                    zeroline=False,
                    showgrid=True,
                    mirror=True,
                    ticklen=4,
                    gridcolor='#ffffff',
                    tickfont=dict(size=10))
        layout = dict(
                    width=1000,
                    height=865,
                    autosize=False,
                    title=metric_name,
                    margin=dict(t=75),
                    showlegend=True,
                    xaxis1=dict(axis, **dict(domain=[0, 1], anchor='y1', showticklabels=True)),
                    yaxis1=dict(axis, **dict(domain=[2 * 0.21 + 0.20, 1], anchor='x1', hoverformat='.2f')))

        fig = go.Figure(data=[table, anomalies_map, Actuals], layout=layout)
        figures.append(fig)
        i += 1

      return figures