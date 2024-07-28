# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px

# Incorporate data
df = pd.read_csv('parsedDF.csv')
categories = ["Powertrain", "Chassis",
               "Drivetrain", "Controls", 
               "BMS", "Inverter", "Aero"]

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Wisconsin Racing Data Viewer'),
    html.Hr(),
    dcc.RadioItems(options=['RRMotorSpeed', 'RLMotorSpeed', 'VehicleSpeed'], value='lifeExp', id='controls-and-radio-item'),
    dcc.Dropdown(options=categories, value="Choose a category"),
    dash_table.DataTable(data=df.to_dict("records"), page_size=6),
    dcc.Graph(figure={}, id='controls-and-graph')
])

# Add controls to build the interaction
@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.line(df, y=col_chosen)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



# from dash import Dash, html, dash_table, dcc
# import pandas as pd
# import plotly.express as px

# # Incorporate data
# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# # Initialize the app
# app = Dash(__name__)

# # App layout
# app.layout = html.Div([
#     html.Div(children='My First App with Data and a Graph'),
#     dash_table.DataTable(data=df.to_dict('records'), page_size=10),
#     dcc.Graph(figure=px.histogram(df, x='continent', y='lifeExp', histfunc='avg'))
# ])

# # Run the app
# if __name__ == '__main__':
#     app.run(debug=True)