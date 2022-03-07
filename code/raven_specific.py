import pandas as pd


def calc_monthly_temp(df, number_of_years):
    """
    Create lists of min, mean and max monthly temperature.
    """
    temp_df = df.groupby(pd.PeriodIndex(df["MESS_DATUM"], freq="M"))["TEMP_MIN"].mean()
    monthly_min_temperature_l = ((temp_df.to_numpy()).reshape(number_of_years,12)).mean(axis=0)
    temp_df = df.groupby(pd.PeriodIndex(df["MESS_DATUM"], freq="M"))["TEMP_MAX"].mean()
    monthly_max_temperature_l = ((temp_df.to_numpy()).reshape(number_of_years,12)).mean(axis=0)
    temp_df = df.groupby(pd.PeriodIndex(df["MESS_DATUM"], freq="M"))["TEMP_AVE"].mean()
    monthly_ave_temperature_l = ((temp_df.to_numpy()).reshape(number_of_years,12)).mean(axis=0)
    monthly_min_temperature = ""
    monthly_max_temperature = ""
    monthly_ave_temperature = ""
    for i in range(12):
        monthly_min_temperature += str(round(monthly_min_temperature_l[i], 2)) + " "
        monthly_max_temperature += str(round(monthly_max_temperature_l[i], 2)) + " "
        monthly_ave_temperature += str(round(monthly_ave_temperature_l[i], 2)) + " "    
    return monthly_min_temperature, monthly_max_temperature, monthly_ave_temperature

def convert_units(df):
    """
    Convert CLOUD_COVER, AIR_PRES, REL_HUMIDITY and SHORTWAVE in units required by Raven.
    """
    # convert air pressure unit from hPa to kPa
    if "AIR_PRES" in df:
        pressure = df["AIR_PRES"].to_list()
        df["AIR_PRES"] = [x/10 if x!=-999 else x for x in pressure]
        df["AIR_PRES"] = df["AIR_PRES"].round(2)
    # convert rel humidity unit from percent to 0...1
    if "REL_HUMIDITY" in df:
        relhumidity = df["REL_HUMIDITY"].to_list()
        df["REL_HUMIDITY"] = [x/100 if x!=-999 else x for x in relhumidity]
        df["REL_HUMIDITY"] = df["REL_HUMIDITY"].round(2)
    # convert short wave radiation into MJ/m²
    if "SHORTWAVE" in df:
        sw = df["SHORTWAVE"].to_list()
        df["SHORTWAVE"] = [x*10000/1000000 if x!=-999 else x for x in sw]
        df["SHORTWAVE"] = df["SHORTWAVE"].round(2)
    # convert cloud cover unit from 0...8 to 0...1
    if "CLOUD_COVER" in df:
        cloudcover = df["CLOUD_COVER"].to_list()
        df["CLOUD_COVER"] = [x/8 if x!=-999 else x for x in cloudcover]
        df["CLOUD_COVER"] = df["CLOUD_COVER"].round(2)
    return df

def write_rvt(df, rvt_name):
    """
    Create new .rvt-file and add header, data and footer acording to RAVEN manual requirements.
    """
    # create file
    myfile = open(f'data/rvt_files_gauges/{rvt_name}.rvt', 'w')
    # add header
    myfile.write(':MultiData')
    myfile.write(f"\n\t2001-01-01 00:00:00 1.0 {len(df)}")
    if len(df.columns) == 9:
        myfile.write(f"\n\t\t:Parameters WIND_VEL CLOUD_COVER AIR_PRES TEMP_AVE REL_HUMIDITY TEMP_MAX TEMP_MIN RAINFALL SNOWFALL")
        myfile.write(f"\n\t\t:Units m/s - kPa degC - degC degC mm/d mm/d")
    if len(df.columns) == 10:
        myfile.write(f"\n\t\t:Parameters WIND_VEL CLOUD_COVER AIR_PRES TEMP_AVE REL_HUMIDITY TEMP_MAX TEMP_MIN RAINFALL SNOWFALL SHORTWAVE")
        myfile.write(f"\n\t\t:Units m/s - kPa degC - degC degC mm/d mm/d MJ/m²/d")
    # add data
    df_list = df.values.tolist()
    for i in range(len(df_list)):
        row_list = df_list[i]
        row_string = ""
        for j in row_list:
            row_string+=str(j)
            row_string+=" "
        myfile.write("\n\t\t"+row_string)
    # add footer
    myfile.write('\n:EndMultiData')
    myfile.close()
    return 0

def write_rvt_rekis(df, rvt_name, scenario):
    """
    Create new .rvt-file and add header, data and footer acording to RAVEN manual requirements.
    """
    myfile = open(f'data/rvt_files_gridpoints/rcp{scenario}/{rvt_name}.rvt', 'w') # create file
    myfile.write(':MultiData') # add header
    myfile.write(f"\n\t2006-01-01 00:00:00 1.0 {len(df)}")
    myfile.write(f"\n\t\t:Parameters TEMP_MAX TEMP_AVE TEMP_MIN REL_HUMIDITY AIR_PRES WIND_VEL RAINFALL SNOWFALL")
    myfile.write(f"\n\t\t:Units degC degC degC - kPa m/s mm/d mm/d")
    
    df_list = df.values.tolist() # add data
    for i in range(len(df_list)):
        row_list = df_list[i]
        row_string = ""
        for j in row_list:
            row_string+=str(j)
            row_string+=" "
        myfile.write("\n\t\t"+row_string)
    
    myfile.write('\n:EndMultiData') # add footer
    myfile.close()
    return 0