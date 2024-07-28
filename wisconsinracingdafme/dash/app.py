import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import requests
from io import StringIO


# Assume you have a DataFrame 'df' with columns 'A', 'B', 'C', 'D'
# df = pd.DataFrame({
#     'A': [1, 2, 3, 4, 5],
#     'B': [2, 3, 4, 5, 6],
#     'C': [3, 4, 5, 6, 7],
#     'D': [4, 5, 6, 7, 72]
# })

# Selection Lists
cars = ["E car"," C Car"]
typegraph = ["Line", "Scatter"]

# Acquire updated Nomenclature from DataConverter Google Sheets
DataConverterSPNomenclature = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vROhUM2sBZQQkgynV69CK53qU13XijuS8bWv12_lNt9gKFAcMNtJAt29T4glKgWy0eoQri0FEB3Nw4W/pub?gid=0&single=true&output=csv')
DataConverterSPNomenclature.raise_for_status()
s=str(DataConverterSPNomenclature.content,'utf-8')
data = StringIO(s) 
nomenclature=pd.read_csv(data)
pivotnom = nomenclature.pivot_table(values="Wisconsin Racing Nomenclature", index=nomenclature.index, columns='Category', aggfunc='first')

teams = list(set(nomenclature['Category'])) # Dash Dropdown



df = pd.read_csv('parsedDF.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='choosecar',
        options=cars,
    ),
    dcc.Dropdown(
        id='chooseteams',
        options=teams,
    ),
    dcc.Dropdown(
        id='xaxis-column',
        options=[{'label': i, 'value': i} for i in df.columns],
    ),
    dcc.Dropdown(
        id='yaxis-column',
        options=[{'label': i, 'value': i} for i in df.columns],
    ),
    dcc.Graph(id='my-graph')
])



@app.callback(
    [Output('xaxis-column', 'options'), 
     Output('yaxis-column', 'options')],    
    Input('chooseteams', 'value')
)
def updateaxesoptions(teamchosen):
    global pivotnom
    sensors1 = pivotnom[teamchosen].dropna() # Dash Dropdown, active textbox?
    sensors2 = pivotnom[teamchosen].dropna() # Dash Dropdown, active textbox?
    return sensors1, sensors2



@app.callback(
    Output('my-graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value')]
)
def update_scatter(xaxis_column_name, yaxis_column_name):
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
    app.run_server(debug=False)#,port=8080,host='0.0.0.0') ## This will enable access on a local network from any device, be careful