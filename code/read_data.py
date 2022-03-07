from datetime import datetime
import pandas as pd


def read_data_klima(filename, start_date, end_date):
    """ 
    Read data file. Rename columns to names specified by RAVEN. Create datetime object for column MESS_DATUM. 
    Drop data rows outside of date frame of interest.
    """
    df = pd.read_csv(filename, sep=';', usecols=["MESS_DATUM","FM","RSK","RSKF","NM","PM","TMK","UPM","TXK","TNK"], 
                    skipinitialspace = True) # skipinitialspace removes whitespace

    df = df.rename(columns={"FM":"WIND_VEL", "RSK":"PRECIP", "NM":"CLOUD_COVER", "PM":"AIR_PRES", "TMK":"TEMP_AVE", 
                            "UPM":"REL_HUMIDITY", "TXK":"TEMP_MAX", "TNK":"TEMP_MIN"})

    datelist = df["MESS_DATUM"].to_list()
    df["MESS_DATUM"] = [datetime.strptime(str(x), '%Y%m%d') if x!=-999 else x for x in datelist]
    df["MESS_DATUM"] = df["MESS_DATUM"]

    df = df.drop(df[df.MESS_DATUM < start_date].index)
    df = df.drop(df[df.MESS_DATUM > end_date].index)
    
    return df

def read_data_solar(filename, start_date, end_date):
    """ 
    Read data file. Rename columns to names specified by RAVEN. Create datetime object for column MESS_DATUM. 
    Drop data rows outside of date frame of interest.
    """
    df = pd.read_csv(filename, sep=';', usecols=["MESS_DATUM","FG_STRAHL"], skipinitialspace = True) # skipinitialspace removes whitespace

    df = df.rename(columns={"FG_STRAHL":"SHORTWAVE"})

    datelist = df["MESS_DATUM"].to_list()
    df["MESS_DATUM"] = [datetime.strptime(str(x), '%Y%m%d') if x!=-999 else x for x in datelist]
    df["MESS_DATUM"] = df["MESS_DATUM"]

    df = df.drop(df[df.MESS_DATUM < start_date].index)
    df = df.drop(df[df.MESS_DATUM > end_date].index)
    
    return df

def read_data_rekis(filename, start_date, end_date):
    """ 
    Read data file. Rename columns to names specified by RAVEN. Create datetime object for column MESS_DATUM. 
    Drop data rows outside of date frame of interest.
    """
    df = pd.read_csv(filename, sep=' ', skiprows=1, usecols=["ta", "mo", "jahr", "TX","TM", "TN", "RF", "RK", "PP", "FF"], skipinitialspace = True) # skipinitialspace removes whitespace
    ta = df["ta"].to_list()
    mo = df["mo"].to_list()
    jahr = df["jahr"].to_list()
    df["MESS_DATUM"] = [datetime.strptime(str(j)+str(m)+str(t), '%Y%m%d') for j,m,t in zip(jahr, mo, ta)]    
    df = df.drop(df[df.MESS_DATUM < start_date].index)
    df = df.drop(df[df.MESS_DATUM > end_date].index)
    df = df.drop(["ta", "mo", "jahr"], axis=1)
    df = df.rename(columns={"TX":"TEMP_MAX", "TM":"TEMP_AVE", "TN":"TEMP_MIN", "RF":"REL_HUMIDITY", 
                            "RK":"PRECIP", "PP":"AIR_PRES", "FF":"WIND_VEL"})
    return df