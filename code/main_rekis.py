import numpy as np
from datetime import datetime
import pandas as pd 

from read_data import read_data_rekis
from consistency_check import consistency_check
from precipitation_corr import split_precip
from raven_specific import convert_units, calc_monthly_temp,  write_rvt_rekis


# Time frame of interest
start_date = datetime(year=2006,month=1,day=1)
end_date = datetime(year=2100,month=12,day=31)

# Read data.
path = "data/metdata/ReKIS/"
scenario = "85"

def Rekis_Processing(filename):
    df = read_data_rekis(path+f"RCP{scenario}/{filename}", start_date, end_date)
    consistency_check(df, start_date, end_date, ["TEMP_MAX", "TEMP_AVE", "TEMP_MIN", "REL_HUMIDITY", "AIR_PRES", "WIND_VEL", "PRECIP", "MESS_DATUM"])
    monthly_min_temperature, monthly_max_temperature, monthly_ave_temperature = calc_monthly_temp(df, 95)
    print(":MonthlyMinTemperature ["+monthly_min_temperature+"]")
    print(":MonthlyMaxTemperature ["+monthly_max_temperature+"]")
    print(":MonthlyAveTemperature ["+monthly_ave_temperature+"]")
    print(filename[34:42])
    if filename[34:42] == "GP_26_09": # Calc yearly temperature of middle grid point.
        temp_df = df.groupby(pd.PeriodIndex(df["MESS_DATUM"], freq="Y"))["TEMP_AVE"].mean()
        np.savetxt(f"data/meanannualtemp_rcp{scenario}.txt", temp_df.values, fmt="%2.2f")
    df = split_precip(df)
    df = convert_units(df)
    write_rvt_rekis(df, filename[34:42], scenario)
    return 0

Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_25_07_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_25_08_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_25_09_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_25_10_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_26_07_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_26_08_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_26_09_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_26_10_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_27_07_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_27_08_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_27_09_r{scenario}_r4_2000-2100.Kli")
Rekis_Processing(f"ReKIS_CMIP5_CanESM2_EPISODES-2018_GP_27_10_r{scenario}_r4_2000-2100.Kli")