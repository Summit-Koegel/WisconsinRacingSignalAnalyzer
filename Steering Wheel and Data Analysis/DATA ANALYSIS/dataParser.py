import csv

def parse_csv(file_path):
    data_dict = {}

    with open(file_path, 'r', encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for _ in range(12):
            next(csv_reader)

        headers = next(csv_reader)[1:]

        for _ in range(12,17):
            next(csv_reader)

        print(headers)

        for row in csv_reader:
            time = float(row[0])
            data_dict[time] = {headers[i - 1]: float(row[i]) for i in range(1, min(len(row), len(headers) + 1))}

    return data_dict


def main():
    file_path = 'suryachassisdynothermostatopen.csv'
    result = parse_csv(file_path)
    if result:
        first_timestamp = min(result.keys())
        last_timestamp = max(result.keys())
    print(f"Runtime: {last_timestamp}")

    rpm1_values = [values["RPM dup 1"] for values in result.values()]
    rpm2_values = [values["RPM dup 1"] for values in result.values()]
    max_rpm1 = max(rpm1_values)
    min_rpm1 = min(rpm1_values)
    max_rpm2 = max(rpm2_values)
    min_rpm2 = min(rpm2_values)

    print(f"Max RPM: {max_rpm1}")
    print(f"Min RPM: {min_rpm1}")
    print(f"Max RPM: {max_rpm2}")
    print(f"Min RPM: {min_rpm2}")

    pressure_values = [values["PressRatio"] for values in result.values()]
    max_pressure = max(pressure_values)
    min_pressure = min(pressure_values)
    print(f"Max Pressure Ratio: {max_pressure}")
    print(f"Min Pressure Ratio: {min_pressure}")


    necct_start_value = result[first_timestamp].get("NECCT")
    necct_end_value = result[last_timestamp].get("NECCT")

    if necct_start_value is not None:
        print(f"NECCT Start Value: {necct_start_value}")

    if necct_end_value is not None:
        print(f"NECCT End Value: {necct_end_value}")

    # for time, values in result.items():
    #     for key, value in values.items():
    #         if(key == "NECCT" and time == 0.02):
    #             print(f"NECCT Start Value: {value}")
    #         elif(key == "NECCT" and time == 140.2):
    #             print(f"NECCT End Value: {value}")



if __name__ == '__main__':
    main()
