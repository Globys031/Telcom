import dash
from dash.dependencies import Output, Input
from dash import dcc
from dash import html
import plotly
import random
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=20)
X.append(1)
Y = deque(maxlen=20)
Y.append(1)

ALLOWED_TYPES = (
    "text", "number", "password", "email", "search",
    "tel", "url", "range", "hidden",
)


app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1*1000, # in miliseconds
            n_intervals=0
        )
        for _ in ALLOWED_TYPES
    ]
)

@app.callback(
    Output(component_id='live-graph', component_property='figure'),
    Input(component_id='graph-update', component_property='n_intervals')
) # '@' simbolis nurodo kad naudojamas zemiau esantis metodas
def update_graph_scatter(self):
    print("test")

    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))

    data = plotly.graph_objs.Scatter(
            x=list(X),
            y=list(Y),
            name='Scatter',
            mode= 'lines+markers'
            )

    axis = dict(
        showline=True,
        zeroline=False,
        showgrid=True,
        mirror=True,
        ticklen=4,
        gridcolor='#ffffff',
        tickfont=dict(size=10))

    layout = dict(
        # width=1000,
        height=400,
        autosize=True,
        title="test",
        margin=dict(t=75),
        showlegend=True,
        xaxis1=dict(axis, **dict(range=[min(X),max(X)], anchor='y1', showticklabels=True)),
        yaxis1=dict(axis, **dict(range=[min(Y),max(Y)], anchor='x1', hoverformat='.2f')))

    return {'data': [data],'layout' : go.Layout(layout)}



if __name__ == '__main__':
  app.run_server(host="127.0.0.1", port=8080, debug=True)