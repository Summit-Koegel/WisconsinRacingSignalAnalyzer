# Import packages
from dash import Dash, Dash, dcc, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import mdfreader
import os
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
from io import StringIO
import base64
import io

Ecar = True
df = pd.DataFrame({})
def convert():
    print("convert")
    # input_path = "ECar_Endurance_2023.MDF"
    # mdf_file = mdfreader.Mdf(input_path)
    # mdf_file.export_to_csv('temp.csv')
    # df = pd.read_csv('../data/zane2.csv', low_memory=False)[1:]
    # df = df.iloc[:50]
    # os.remove('temp.csv')
    # print(df.head())
    
    data_converter_path = "../data/DataConverter.csv"
    data_converter = {}

    with open(data_converter_path, 'r') as converter_file:
        next(converter_file)

        for line in converter_file.readlines():
            parts = line.strip().split(',')
            if len(parts) >= 7:
                category = parts[0]
                signal1 = parts[1]
                signal2 = parts[2]
                signal3 = parts[3]
                signal4 = parts[4]
                nomenclature = parts[5]
                units = parts[6]
                priority = parts[7]

                data_converter[nomenclature] = {
                    'Category': category,
                    'Signal 1': signal1,
                    'Signal 2': signal2,
                    'Signal 3': signal3,
                    'Signal 4': signal4,
                    'Nomenclature': nomenclature,
                    'Units': units,
                    'Priority': priority
                }
                
    return data_converter
        
def findValues(data_converter): 
    global df
    print("findvaluesrunning")
    first_line = df.columns.tolist()
    parsedDF = "parsedDF.csv"
    for signal_name in first_line:
        found_matching_signal = False
        for nomenclature, converter_info in data_converter.items():
            if signal_name == "t":
                continue
            if signal_name == "Time":
                df["Time"] = df[signal_name]  # Add the 'Time' column to the dataframe
                found_matching_signal = True
                break
            if (signal_name == converter_info['Signal 1'] or
                signal_name == converter_info['Signal 2'] or
                signal_name == converter_info['Signal 3'] or
                signal_name == converter_info['Signal 4']):
                new_column_name = converter_info['Nomenclature'] + '  ' + converter_info['Units']
                df.rename(columns={signal_name: new_column_name}, inplace=True)
                found_matching_signal = True
                break
        if not found_matching_signal:
            df.drop(columns=signal_name, axis = 2, inplace=True)
    df.to_csv(parsedDF, index=False)
    return df
    
def calculate_summary_statistics(df):
    print("summarycalculated")
    global Ecar
    if(Ecar == True):
        average_speed = df['VehicleSpeed  mph'].apply(pd.to_numeric, errors='ignore').mean()
        max_ay = df['AccelY  g'].apply(pd.to_numeric, errors='ignore').max()
        max_ax = df['AccelX  g'].apply(pd.to_numeric, errors='ignore').max()
        return average_speed, max_ay, max_ax
    elif(Ecar == False):
        above_1000 = 0
        running_time = df['EngineRPM  RPM'].apply(pd.to_numeric, errors='coerce')
        for rt in running_time:
            if rt >= 1000:
                above_1000 += 0.1
        return above_1000
        
def write_to_file(average_speed="", max_ay="", max_ax="", running_time="", filename=""):
    print("writetofile")
    global Ecar
    with open(filename, 'w') as f:
        if Ecar:
            f.write(f"Average Speed: {average_speed}\n")
            f.write(f"Max AY (Acceleration Y): {max_ay}\n")
            f.write(f"Max AX (Acceleration X): {max_ax}\n")
        else:
            f.write(f"Running Time(above 1000 RPM): {running_time} seconds\n")

def main():
    print("mainrun")
    global Ecar    
    # df = pd.read_csv('parsedDF.csv')

    categories = ["Powertrain", "Chassis",
                "Drivetrain", "Controls", 
                "BMS", "Inverter", "Aero"]

    
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
    
    # Initialize the app
    app = Dash(__name__)
    print("App Initialized")
    app.layout = html.Div([
        html.Div(children='Wisconsin Racing Data Viewer', style={'fontSize': 30}),
            html.Hr(),
            dcc.Dropdown(
                id='choosecar',
                options=cars,
            ),
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select CSV/MDF File')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(id='output-data-upload'),
    ])
    
    @app.callback(
        Output('output-data-upload', 'value'),
        [Input('choosecar', 'value')]
    )
    def updateEcar(value):
        global Ecar
        print("updateEcar")
        if value == "E car":
            Ecar = True
        else:
            Ecar = False
    

    @app.callback(
        Output('output-data-upload', 'children'),
        [Input('upload-data', 'contents'),
        Input('upload-data', 'filename')]
    )
    def update_output(contents, filename):
        global df
        print("print updateoutput")
        if(Ecar == False):
            if contents is not None:
                content_type, content_string = contents.split(',')
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        else:
            if filename is not None:    
                mdf_file = mdfreader.Mdf(filename)
                mdf_file.export_to_csv('temp.csv')
                df = pd.read_csv('temp.csv', low_memory=False)[1:]
                df = df.iloc[:50]
            # Process the uploaded file and update the layout accordingly
        print(df)
        data_converter = convert()
        print(df)
        findValues(data_converter)
        print(df)
        print("Summary Statistics:")
        if Ecar == True:
            average_speed, max_ay, max_ax = calculate_summary_statistics(df)
            print(f"Average Speed: {average_speed}")
            print(f"Max AY (Acceleration Y): {max_ay}")
            print(f"Max AX (Acceleration X): {max_ax}")
            write_to_file(average_speed, max_ay, max_ax, None, "ECarSummaryStatistics.txt")
        else:
            running_time = calculate_summary_statistics(df)
            print(f"Running Time(above 1000 RPM): {running_time} seconds")
            write_to_file(None, None, None, running_time, "CCarSummaryStatistics.txt")
        # global df  
        # df = pd.read_csv('parsedDF.csv')
    
        print(df)
        print("dataFrame printed")
        return html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                placeholder="Select a sensor for the X Axis",
            ),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in df.columns],
                placeholder="Select a sensor for the Y Axis",
            ),
            html.Div([
            dcc.Graph(id='my-graph'),
            dash_table.DataTable(data=df.to_dict("records"), page_size=6)]
            ,hidden=True, id='graphtablediv')
        ], hidden=False, id='maindiv')
    
    @app.callback(
        [Output('xaxis-column', 'options'), 
        Output('yaxis-column', 'options')],    
        Input('chooseteams', 'value'),
    )
    def updateaxesoptions(teamchosen):
        print("updateaxes")
        global pivotnom
        sensors1 = pivotnom[teamchosen].dropna() # Dash Dropdown, active textbox?
        sensors2 = pivotnom[teamchosen].dropna() # Dash Dropdown, active textbox?
        return sensors1, sensors2
    
    # df, data_converter = convert()
    # df2 = findValues(df, data_converter)
    # print("Summary Statistics:")
    # if(Ecar == True):
    #     average_speed,max_ay,max_ax = calculate_summary_statistics(df2)
    #     print(f"Average Speed: {average_speed}")
    #     print(f"Max AY (Acceleration Y): {max_ay}")
    #     print(f"Max AX (Acceleration X): {max_ax}")
    # else:
    #     running_time = calculate_summary_statistics(df2)
    #     print(f"Running Time(above 1000 RPM): {running_time} seconds")
    
    

    # Add controls to build the interaction
    # @callback(
    #     Output(component_id='controls-and-graph', component_property='figure'),
    #     Input(component_id='controls-and-radio-item', component_property='value')
    # )
  


    @app.callback([
        Output('my-graph', 'figure'), 
        Output('graphtablediv', 'hidden')],
        [Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value')]
    )
    def update_scatter(xaxis_column_name, yaxis_column_name):
        global df
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
        }, False

    if __name__ == '__main__':
        app.run_server(debug=False)#,port=8080,host='0.0.0.0') ## This will enable access on a local network from any device, be careful

if __name__ == '__main__':
    main()