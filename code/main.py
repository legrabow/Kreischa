import os, glob
import numpy as np
import pandas as pd
from datetime import datetime
import math

from read_data import read_data_klima, read_data_solar
from consistency_check import  consistency_check
from precipitation_corr import preci_corr
from raven_specific import calc_monthly_temp, convert_units, write_rvt


# List of filenames of interest
klima_files = glob.glob('data/metdata/dwd_klima/produkt_klima_tag*.txt')
solar_files = glob.glob('data/metdata/dwd_solar/produkt_st_tag*.txt')

# Time frame of interest
start_date = datetime(year=2001,month=1,day=1)
end_date = datetime(year=2020,month=12,day=31)

# Stations of interest
stations = ["03166", "00853", "05779", "06129", "02985", "01050", "00991", "00314", "01048", "03811"]

# Location's influece on precipitation messurement: 0 (freie Lage), 1 (leicht geschützt), 2 (mäßig geschützt), 3 (stark geschützt)
geschuetzt = {"00314":0, "00853":0, "00991":0, "01048":0, "01050":1, "02985":1, "03166":0, "03811":1, "05779":0, "06129":2}

# Precipitation correction parameters [Tab. 16 Richter (1995)]
koeff_b = [[0.345, 0.34, 0.343, 0.535, 0.72],       # freie Lage
            [0.31, 0.28, 0.295, 0.39, 0.51],        # leicht geschützt
            [0.28,0.24,0.26,0.305,0.33],            # mäßig geschützt
            [0.245,0.19,0.218,0.185,0.21]]          # stark geschützt

# Write header of rvt station data.
if os.path.exists("data/rvt_files_gauges/gauges.rvt"):
    os.remove("data/rvt_files_gauges/gauges.rvt") # remove existing file to prevent apending multiple times
with open('data/rvt_files_gauges/gauges.rvt', 'a') as gaugefile:
    gaugefile.write("#--------------------------------------------\n# Raven Time Series Input file\n#--------------------------------------------")


print("\n1) Read data.\n")
df_03166 = read_data_klima(klima_files[0], start_date, end_date)
df_00853 = read_data_klima(klima_files[1], start_date, end_date)
df_05779 = read_data_klima(klima_files[2], start_date, end_date)
df_06129 = read_data_klima(klima_files[3], start_date, end_date)
df_02985 = read_data_klima(klima_files[4], start_date, end_date)
df_01050 = read_data_klima(klima_files[5], start_date, end_date)
df_00991 = read_data_klima(klima_files[6], start_date, end_date)
df_00314 = read_data_klima(klima_files[7], start_date, end_date)
df_01048 = read_data_klima(klima_files[8], start_date, end_date)
df_03811 = read_data_klima(klima_files[9], start_date, end_date)
df_00853_sol = read_data_solar(solar_files[0], start_date, end_date)
df_01048_sol = read_data_solar(solar_files[1], start_date, end_date)


print("\n2) Check consistency\n")
dict_03166_nan = consistency_check(df_03166, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_00853_nan = consistency_check(df_00853, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_05779_nan = consistency_check(df_05779, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_06129_nan = consistency_check(df_06129, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_02985_nan = consistency_check(df_02985, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_01050_nan = consistency_check(df_01050, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_00991_nan = consistency_check(df_00991, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_00314_nan = consistency_check(df_00314, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_01048_nan = consistency_check(df_01048, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_03811_nan = consistency_check(df_03811, start_date, end_date, ["WIND_VEL", "PRECIP", "RSKF", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"])
dict_00853_sol_nan = consistency_check(df_00853_sol, start_date, end_date, ["SHORTWAVE"])
dict_01048_sol_nan = consistency_check(df_01048_sol, start_date, end_date, ["SHORTWAVE"])


print("\n3.1) Correct inconsistency in climate data by spatial interpolation\n")
distancematrix = pd.read_csv("data/dwdstations_distance_matrix.csv", sep=',', usecols=["InputID","TargetID","Distance"]) # created with QGIS
inp = distancematrix["InputID"].tolist()
targ = distancematrix["TargetID"].tolist()
distancematrix["Index"] = [f"{str(inp[x]).zfill(5)}-{str(targ[x]).zfill(5)}" for x in range(len(distancematrix["InputID"]))]
distancematrix = distancematrix.set_index("Index")

for col in ["WIND_VEL", "PRECIP", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE","REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN"]:
    for day in range(len(dict_03166_nan["MESS_DATUM"])): # Read values and split into nan and reference values for correction.
        # Get values from all stations.
        val_list = []
        for s in stations:
            globals()["v_"+s] = globals()["dict_"+s+"_nan"][col][day]
            val_list.append(globals()["v_"+s])
        # Split values in nan's and reference values.
        nanlist = []
        refdict = {"id":[], "val":[]}
        for i in range(len(val_list)):
            if math.isnan(val_list[i]):
                nanlist.append(stations[i])
            else:
                refdict["id"].append(stations[i])
                refdict["val"].append(val_list[i])
        # Correct nan's.
        for nanstation in nanlist:
            numerator = 0
            denominator = 0
            for j in range(len(refdict["id"])):
                id_refstation = refdict["id"][j]
                val_refstation = refdict["val"][j]
                w = distancematrix.loc[nanstation+"-"+id_refstation, 'Distance']
                numerator+=w*val_refstation
                denominator += w
            newval = round(numerator/denominator, 1)
            globals()["dict_"+nanstation+"_nan"][col][day] = newval # insert new value

for s in stations:
    globals()["df_"+s] = pd.DataFrame.from_dict(globals()["dict_"+s+"_nan"], orient = "columns")


print("\n3.2) Correct solar inconsistency by interpolate NaN's along column axis.\n")
df_00853_sol = pd.DataFrame.from_dict(dict_00853_sol_nan, orient = "columns")
df_01048_sol = pd.DataFrame.from_dict(dict_01048_sol_nan, orient = "columns")
df_00853_sol = df_00853_sol.interpolate(method="pad", axis="rows", limit=200)
df_01048_sol = df_01048_sol.interpolate(method="pad", axis="rows", limit=200)


print("\n4) Calculate monthly min/max/ave temperature.\n")
tmin_03166, tmax_03166, tave_03166 = calc_monthly_temp(df_03166, number_of_years=20)
tmin_00853, tmax_00853, tave_00853 = calc_monthly_temp(df_00853, number_of_years=20)
tmin_05779, tmax_05779, tave_05779 = calc_monthly_temp(df_05779, number_of_years=20)
tmin_06129, tmax_06129, tave_06129 = calc_monthly_temp(df_06129, number_of_years=20)
tmin_02985, tmax_02985, tave_02985 = calc_monthly_temp(df_02985, number_of_years=20)
tmin_01050, tmax_01050, tave_01050 = calc_monthly_temp(df_01050, number_of_years=20)
tmin_00991, tmax_00991, tave_00991 = calc_monthly_temp(df_00991, number_of_years=20)
tmin_00314, tmax_00314, tave_00314 = calc_monthly_temp(df_00314, number_of_years=20)
tmin_01048, tmax_01048, tave_01048 = calc_monthly_temp(df_01048, number_of_years=20)
tmin_03811, tmax_03811, tave_03811 = calc_monthly_temp(df_03811, number_of_years=20)

temp_arr = np.array([
        [tmin_03166, tmax_03166, tave_03166],
        [tmin_00853, tmax_00853, tave_00853],
        [tmin_05779, tmax_05779, tave_05779],
        [tmin_06129, tmax_06129, tave_06129],
        [tmin_02985, tmax_02985, tave_02985],
        [tmin_01050, tmax_01050, tave_01050],
        [tmin_00991, tmax_00991, tave_00991],
        [tmin_00314, tmax_00314, tave_00314],
        [tmin_01048, tmax_01048, tave_01048],
        [tmin_03811, tmax_03811, tave_03811]
    ])


print("\n5) Calculate precipitation correction and split into into rain/snow. Convert units. Check again for NaN's.\n")
for s in stations:    
    globals()["df_"+s+"_corr"] = preci_corr(globals()["df_"+s], s, geschuetzt, koeff_b) 
    globals()["df_"+s+"_corr"] = convert_units(globals()["df_"+s+"_corr"])
    print(f"\nStation {s}\n",globals()["df_"+s+"_corr"].isna().sum())
    

print("\n6. Write rvt files. \n")
stationsno_list = ["03166", "00853", "05779", "06129", "02985", "01050", "00991", "00314", "01048", "03811"]
for i in range(len(stationsno_list)):
    stationsno = stationsno_list[i]
    data = pd.read_csv(f"data/metdata/dwd_klima/Metadaten_Geographie_{stationsno}.txt", delimiter=";", encoding= 'unicode_escape')
    meatadata_list = data.iloc[-1].tolist()
    id, elev, lat, lon, date1, date2, stationsname =  meatadata_list

    with open('data/rvt_files_gauges/gauges.rvt', 'a') as metadata:
        metadata.write(f"\n:Gauge {stationsname} (ID:{stationsno})")
        metadata.write(f"\n\t:Latitude {lat}")
        metadata.write(f"\n\t:Longitude {lon}")
        metadata.write(f"\n\t:Elevation {elev}")
        metadata.write(f"\n\t: MonthlyAveTemperature [{temp_arr[i][0][:-1]}]") # [-1]: remove last whitespace
        metadata.write(f"\n\t: MonthlyMinTemperature [{temp_arr[i][1][:-1]}]")
        metadata.write(f"\n\t: MonthlyMaxTemperature [{temp_arr[i][2][:-1]}]")
        metadata.write(f"\n\tRedirectToFile dwd_{stationsno}.rvt")
        metadata.write('\n:EndGauge')

# write rvt multidata
for s in stations:
    if s == "00853":
        globals()["df_"+s+"_corr"]["SHORTWAVE"] = [x*10000/1000000 if x!=-999 else x for x in df_00853_sol["SHORTWAVE"]]
    if s == "01048":
        globals()["df_"+s+"_corr"]["SHORTWAVE"] = [x*10000/1000000 if x!=-999 else x for x in df_01048_sol["SHORTWAVE"]]  
    write_rvt(globals()["df_"+s+"_corr"], f"dwd_{s}")