# WisconsinRacingDAFME

dataConverterConverter.py is the original code from Summit

dataConverter.csv, WR224.dbc, and an MDF are necessary to run dataConverterConverter.py

Eventually the dataConverter will be capable of converting data from both the MDF and the EVO CSV files

parsedDF.csv is the output from dataConverterConverter.py

dataAnalysis.ipynb is a test notebook for creating visualizations and using the dataConverter

app.py is the code for the dash board, it uses the Dash Python Library to generate the User Interface: https://dash.plotly.com/

- app.py acquires updated Nomenclature data from the DataConverter Google Sheet
- It also organizes teams and sorts the available sensors based on that
- Currently there is a bug due to some mismatch between the availability of sensors in parsedDf.csv and the Nomenclature   
- Currently, the car picker has no additional functionality, not really sure if its necessary since picking a team should sort most of the relevant sensors