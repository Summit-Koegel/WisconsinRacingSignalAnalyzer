import pandas as pd
import numpy as np
import mdfreader
import os

def convert():
    input_path = "ECar_Endurance_2023.MDF"
    mdf_file = mdfreader.Mdf(input_path)
    mdf_file.export_to_csv('temp.csv')
    df = pd.read_csv('temp.csv', low_memory=False)[1:]
    df = df.iloc[:50]
    # os.remove('temp.csv')
    # print(df.head())
    
    data_converter_path = "dataConverter.csv"
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
                
    return df, data_converter
        
def findValues(df, data_converter ):  
    first_line = df.columns.tolist()
    parsedDF = "parsedDF.csv"
    for signal_name in first_line:
        found_matching_signal = False
        for nomenclature, converter_info in data_converter.items():
            if signal_name == "t":
                continue
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
    df['VehicleSpeed  mph'] = pd.to_numeric(df['VehicleSpeed  mph'], errors='coerce')
    non_zero_values = df[df['VehicleSpeed  mph'] != 0]
    average_speed = non_zero_values['VehicleSpeed  mph'].mean()
    # average_speed = df['VehicleSpeed  mph'].apply(pd.to_numeric, errors='ignore').mean()
    max_ay = df['AccelY  g'].apply(pd.to_numeric, errors='ignore').max()
    max_ax = df['AccelX  g'].apply(pd.to_numeric, errors='ignore').max()

    return average_speed, max_ay, max_ax

def main():
    df, data_converter = convert()
    df2 = findValues(df, data_converter)
    average_speed,max_ay,max_ax = calculate_summary_statistics(df2)
    print("Summary Statistics:")
    print(f"Average Speed: {average_speed}")
    print(f"Max AY (Acceleration Y): {max_ay}")
    print(f"Max AX (Acceleration X): {max_ax}")

if __name__ == '__main__':
    main()