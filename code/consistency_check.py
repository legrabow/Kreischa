import sys
from datetime import timedelta
import pandas as pd
import numpy as np


def consistency_check(df, start_date, end_date, col_list):
    """
    Check for NaN's in raw data. Check for missing dates and add new line with -999 labeled values for each missing date. 
    Check for missing values labeled with -999
    
    Parameters:
        pandas.DataFrame df : meteorological data
        datetime start_date : defines time frame of interest 
        datetime end_time : defines time frame of interest
        list col_list : list of column names
        
    Returns:
        pandas.DataFrame df : meteorological data containing NaN's instead of any missing values
    """
    # Check for NaN's in raw data.
    if df.isnull().values.any() == True:
        sys.exit("Raw data contains NaN.")
    else:
        print("Raw data contains no NaN.")
    
    # Check for missing dates and add new line with -999 labeled values for each missing date.
    data = df.to_numpy()
    colnames = list(df.columns)
    diff = end_date-start_date
    number_days = 1+diff.days
    if number_days != len(df):
        daylist = []
        datelist = data[:,0]
        datelist = [d.strftime("%Y-%m-%d") for d in datelist]
        for i in range(number_days):
            day_ref_dt = start_date + timedelta(days=i)
            day_ref = day_ref_dt.strftime("%Y-%m-%d")
            if day_ref not in datelist:
                daylist.append(day_ref)
                newline = np.array((day_ref_dt, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0, -999.0))
                data = np.insert(data, i, newline, axis=0)            
    else: # df contains no missing days.
        daylist = []
    df = pd.DataFrame(data, columns=colnames)
    print(f"Number of missing rows: {len(daylist)}")
    
    # Print number of values labeled with -999 columnwise.
    dict999 = {k:[] for k in col_list}
    for colname in col_list:
        x = df[colname].value_counts(ascending=False)
        if -999 in x.index:
            dict999[colname].append(x[-999])
        else:
            dict999[colname].append(0)
    print("Check for missing values labeled with -999:", dict999)

    # Replace all values labeled -999 with nan.
    df = df.replace(-999, np.nan)

    return df.to_dict("list")