import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Assume you have a DataFrame 'df' with columns 'A', 'B', 'C', 'D'
# df = pd.DataFrame({
#     'A': [1, 2, 3, 4, 5],
#     'B': [2, 3, 4, 5, 6],
#     'C': [3, 4, 5, 6, 7],
#     'D': [4, 5, 6, 7, 72]
# })

df = pd.read_csv('data/parsedDF.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='A'
    ),
    dcc.Dropdown(
        id='yaxis-column',
        options=[{'label': i, 'value': i} for i in df.columns],
        value='B'
    ),
    dcc.Graph(id='my-graph')
])

@app.callback(
    Output('my-graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')]
)
def update_graph(xaxis_column_name, yaxis_column_name):
    return {
        'data': [go.Scatter(
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            
        )],
        'layout': go.Layout(
            xaxis={'title': xaxis_column_name},
            yaxis={'title': yaxis_column_name},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=False)#,port=8080,host='0.0.0.0')