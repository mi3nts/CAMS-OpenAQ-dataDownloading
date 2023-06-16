# conda env = cams

import cdsapi
from datetime import datetime
import datetime
import os

start_date = datetime.datetime(2020, 10, 1, 0)
end_date = datetime.datetime(2020, 10, 1, 3)

data_save_path = '/Users/prabu/Desktop/ECMWF_CAMS_data/data/'

# comment one variable list to download the other variable list
'''
# Single level and multi level data
variable = ['10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
            '2m_temperature', 'black_carbon_aerosol_optical_depth_550nm', 'carbon_monoxide',
            'dust_aerosol_0.03-0.55um_mixing_ratio', 'dust_aerosol_0.55-0.9um_mixing_ratio', 'dust_aerosol_0.9-20um_mixing_ratio',
            'dust_aerosol_optical_depth_550nm', 'ethane', 'formaldehyde',
            'hydrogen_peroxide', 'hydrophilic_black_carbon_aerosol_mixing_ratio', 'hydrophilic_organic_matter_aerosol_mixing_ratio',
            'hydrophobic_black_carbon_aerosol_mixing_ratio', 'hydrophobic_organic_matter_aerosol_mixing_ratio', 'hydroxyl_radical',
            'isoprene', 'land_sea_mask', 'mean_sea_level_pressure',
            'nitric_acid', 'nitrogen_dioxide', 'nitrogen_monoxide',
            'organic_matter_aerosol_optical_depth_550nm', 'ozone', 'particulate_matter_10um',
            'particulate_matter_1um', 'particulate_matter_2.5um', 'peroxyacetyl_nitrate',
            'propane', 'sea_salt_aerosol_0.03-0.5um_mixing_ratio', 'sea_salt_aerosol_0.5-5um_mixing_ratio',
            'sea_salt_aerosol_5-20um_mixing_ratio', 'sea_salt_aerosol_optical_depth_550nm', 'specific_humidity',
            'sulphate_aerosol_mixing_ratio', 'sulphate_aerosol_optical_depth_550nm', 'sulphur_dioxide',
            'surface_geopotential', 'surface_pressure', 'temperature',
            'total_aerosol_optical_depth_1240nm', 'total_aerosol_optical_depth_469nm', 'total_aerosol_optical_depth_550nm',
            'total_aerosol_optical_depth_670nm', 'total_aerosol_optical_depth_865nm', 'total_column_carbon_monoxide',
            'total_column_ethane', 'total_column_formaldehyde', 'total_column_hydrogen_peroxide',
            'total_column_hydroxyl_radical', 'total_column_isoprene', 'total_column_methane',
            'total_column_nitric_acid', 'total_column_nitrogen_dioxide', 'total_column_nitrogen_monoxide',
            'total_column_ozone', 'total_column_peroxyacetyl_nitrate', 'total_column_propane',
            'total_column_sulphur_dioxide', 'total_column_water_vapour']
'''

# Slow access multi level chemical
variable = ['acetone', 'acetone_product', 'aldehydes', 'amine', 'ammonia', 'ammonium','dimethyl_sulfide', 'dinitrogen_pentoxide', 
            'ethanol', 'ethene', 'formic_acid', 'hydroperoxy_radical', 'lead', 'methacrolein_mvk', 'methacrylic_acid',
            'methane_chemistry', 'methane_sulfonic_acid', 'methanol', 'methyl_glyoxal', 'methyl_peroxide', 'methylperoxy_radical',
            'nitrate', 'nitrate_radical', 'olefins', 'organic_ethers', 'organic_nitrates', 'paraffins', 'pernitric_acid', 
            'peroxides', 'peroxy_acetyl_radical', 'propene', 'radon', 'stratospheric_ozone_tracer', 'terpenes']



current_date = start_date

c = cdsapi.Client()
def dataDownload(date, time, path):
    print(date, time, path)
    c.retrieve(
        'cams-global-reanalysis-eac4',
        {
            'date': date,
            'format': 'grib',
            'variable': variable,
            'area': [90, -180, -90, 180],
            'time': time,
            'model_level': '60',
            'pressure_level': '1000',
        },
        path)

while current_date <= end_date:
    date_time = current_date.strftime("%Y-%m-%d %H:%M:%S")
    year, month, day, hour = str(current_date.year), date_time[5:7], current_date.strftime("%-d"), date_time[11:13]
    date = date_time[0:10]
    time = date_time[11:16]

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

    path = data_save_path + year + '/' + month + '/' + day + '/' + hour +'.grib'

    dataDownload(date, time, path)
    current_date += datetime.timedelta(hours=3)

