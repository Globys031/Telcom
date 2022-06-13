# Telcom

Requires python 3.0 and up, and multiple modules installed:
```
pip install nbformat numpy pandas matplotlib sklearn warnings dash
```

### How data is portrayed in the table:

- gray - not an anomaly
- yellow - a small anomaly (can be safely ignored)
- red - anomaly
- % change shows how much the data in the row above differs from the data in the row below

As for the graph, both the yellow (insignifcant) and the red anomalies are portrayed as red

**Note** that the matplotlib graph shows outliers based on all values. The separate tables
shows further in detail each attribute values that's considered an anomaly

### Sources used as reference:

https://pythonprogramming.net/live-graphs-data-visualization-application-dash-python-tutorial/

https://medium.com/analytics-vidhya/plotting-multiple-figures-with-live-data-using-dash-and-plotly-4f5277870cd7

https://dash.plotly.com/live-updates