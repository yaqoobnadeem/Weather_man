import os
from datetime import datetime

def check_numeric(data):
    try:
        float(data)
        return True
    except ValueError:
        return False

def analyze_rows(data):
    lengthofdata = len(data)
    for x in range(lengthofdata):
        for item in data[x]:
            if check_numeric(item):
                return x-1
    return None


def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%B %d ')
    except ValueError:
        return date_str

def monthcheck(name):

    nameofmonths = ["Jan", "Feb", "Mar", "Apr", "May", "Jun","Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    firstthree = name[:3]
    for x in nameofmonths:
        if x == firstthree:
            return True


def Display(Year, highest_temp, lowest_temp, highest_humidity, htemp_dates_map, ltemp_dates_map, hutemp_dates_map):
    print(f"            {Year}          ")
    htemp_dates = htemp_dates_map.get(highest_temp, [])
    print(f"Highest Maximum Temperature: {highest_temp}°C on {', '.join(htemp_dates)}")
    ltemp_dates = ltemp_dates_map.get(lowest_temp, [])
    print(f"Lowest Minimum Temperature: {lowest_temp}°C on {', '.join(ltemp_dates)}")
    hutemp_dates = hutemp_dates_map.get(highest_humidity, [])
    print(f"Highest Humidity: {highest_humidity}% on {', '.join(hutemp_dates)}")

def WeatherProcessing(filepath):

    filelist = os.listdir(filepath)
    while True:
        try:
            Year = int(input("\n\nEnter the Year For Generating Weather Data Report: "))
            if Year < 1000 or Year > 9999:
                print("Please enter a valid 4-digit year.")
                continue
            matchinglist = [file for file in filelist if f"_{Year}" in file]
            if  matchinglist:
                break
            else:
                print(f"No files found for the year {Year}. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")
            continue     

    
    # while True:
    #     try:
    #         Month = input(f"\nEnter the Month For the {Year} For Generating Weather Data Report: ").strip().title()
    #         if monthcheck(Month):
    #             month_prefix = Month[:3]
    #             matching_month_files = [file for file in matchinglist if f"_{month_prefix}" in file]
    #             if matching_month_files:
    #                 break
    #             else:
    #                 print(f"Month file is not available for {Month}. Please try again.")
    #         else:
    #             print(f"Invalid month name. Please try again.")
    #     except ValueError:
    #         print("Invalid input. Please enter a valid Month.")



    highest_temp = -1000
    lowest_temp = 1000
    highest_humidity = -1

    htemp_dates_map = {}
    ltemp_dates_map = {}
    hutemp_dates_map = {}
    replacement_value = 0
    for file in matchinglist:
        Datacollection = []
        Path = os.path.join(filepath, file)
        with open(Path, 'r') as f:
            for line in f:
                row = line.strip().split(',')
                Datacollection.append(row)

        if not Datacollection:
            print(f"No data found in the file {file}.")
            continue

        header_columns_index = analyze_rows(Datacollection)
        if header_columns_index is None:
            print(f"Header row not found in the file {file}.")
            continue

        headers = Datacollection[header_columns_index]
        max_temps = []
        min_temps = []
        humidities = []
        dates = []


        for row in Datacollection[header_columns_index+1:]:

            try:
                date_str = row[0]
                date_formatted = format_date(date_str)
                row = [replacement_value if cell == '' else cell for cell in row]
                max_temp = float(row[headers.index('Max TemperatureC')])

                min_temp = float(row[headers.index('Min TemperatureC')])


                humidity = float(row[headers.index('Max Humidity')])

                
                dates.append(date_formatted)
                max_temps.append(max_temp)
                min_temps.append(min_temp)
                humidities.append(humidity)

            except (ValueError, IndexError):
                continue


        max_index = max_temps.index(max(max_temps))
        current_max_temp = max_temps[max_index]

        if current_max_temp > highest_temp:
            highest_temp = current_max_temp
            htemp_dates_map[highest_temp] = [dates[max_index]]
        elif current_max_temp == highest_temp:
            htemp_dates_map.setdefault(highest_temp, []).append(dates[max_index])
    

        min_index = min_temps.index(min(min_temps))
        current_min_temp = min_temps[min_index]

        if current_min_temp < lowest_temp:
            lowest_temp = current_min_temp
            ltemp_dates_map[lowest_temp] = [dates[min_index]]
        elif current_min_temp == lowest_temp:
            ltemp_dates_map.setdefault(lowest_temp, []).append(dates[min_index])


        humidity_index = humidities.index(max(humidities))
        current_max_humidity = humidities[humidity_index]

        if current_max_humidity > highest_humidity:
            highest_humidity = current_max_humidity
            hutemp_dates_map[highest_humidity] = [dates[humidity_index]]
        elif current_max_humidity == highest_humidity:
            hutemp_dates_map.setdefault(highest_humidity, []).append(dates[humidity_index])

    Display(Year, highest_temp, lowest_temp, highest_humidity, htemp_dates_map, ltemp_dates_map, hutemp_dates_map)

while True:
    print(" -------------------------------------------------------------------------")
    print("|                                                                         |")
    print("|                             WEATHER-MAN                                 |")
    print("|                                                                         |")
    print("|                                                                         |")
    print("|                      City Weather Data Report                           |")
    print("|                                                                         |")
    print("| Press 1 :: Dubai Weather                                                |")
    print("| Press 2 :: Lahore Weather                                               |")
    print("| Press 3 :: Murree Weather                                               |")
    print("| Press 4 :: For Exit                                                     |")
    print(" -------------------------------------------------------------------------")
    Selection = int(input("\n| Which City Do You Want to View : "))

    if Selection == 1:
        print("                     Dubai Weather \n")
        fpath = r"C:\Users\HP\OneDrive\Desktop\data\Dubai_weather"
        WeatherProcessing(fpath)

    elif Selection == 2:
        print("                     Lahore Weather \n")
        fpath = r"C:\Users\HP\OneDrive\Desktop\data\lahore_weather"
        WeatherProcessing(fpath)

    elif Selection == 3:
        print("                     Murree Weather \n")
        fpath = r"C:\Users\HP\OneDrive\Desktop\data\Murree_weather"
        WeatherProcessing(fpath)
    elif Selection == 4:
        break
    else:
        print("Wrong Choice, Try Again.")
        continue