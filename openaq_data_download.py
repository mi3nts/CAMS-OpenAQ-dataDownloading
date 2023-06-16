# conda env = cams

import openaq
from datetime import datetime
import datetime
import os
import pandas as pd

start_date = datetime.datetime(2020, 10, 1, 2)
end_date = datetime.datetime(2020, 10, 1, 4)
data_save_path = '/Users/prabu/Desktop/check_openAQ/data/'


current_date = start_date

api = openaq.OpenAQ()
country_code = api.countries(limit=10000, df=True)
country_names = country_code['code'].tolist()
filtered_country_list = [item for item in country_names if item != '']
# filtered_country_list = ['US', 'IN']


def dataDownload(path, crt, old):
    datasets = []  # List to store the datasets
    for country in filtered_country_list:
        try:
            data = api.measurements(country=country, parameter='pm25', date_from=old, date_to=crt, df=True, limit=10000)
            datasets.append(data)
        except Exception as e:
            print("An error occurred:", e, "on", crt, "country =", country)
    combined_data = pd.concat(datasets)
    combined_data.to_csv(path)


while current_date <= end_date:
    date_time = current_date.strftime("%Y-%m-%d %H:%M:%S")
    old_date_time = current_date - datetime.timedelta(hours=1)
    year, month, day, hour = str(current_date.year), date_time[5:7], current_date.strftime("%-d"), date_time[11:13]

    try:
        os.mkdir(data_save_path + year)
    except FileExistsError:
        print(year + " year folder exists")
    try:
        os.mkdir(data_save_path + year + '/' + month)
    except FileExistsError:
        print(month + " month folder exists")
    try:
        os.mkdir(data_save_path + year + '/' + month + '/' + day)
    except FileExistsError:
        print(day + " day folder exists")

    path = data_save_path + year + '/' + month + '/' + day + '/' + hour +'_OpenAQ_PM25.csv'
    
    try:
        dataDownload(path, current_date, old_date_time)
    except Exception as e:
        print("An error occurred:", e)
    
    current_date += datetime.timedelta(hours=1)
