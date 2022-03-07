import math


def preci_corr(df_new, stationsno, geschuetzt, koeff_b):
    """ 
    Correct precipitation (Richter) and split precipitation into rain/snow.
    """
    geschuetztheit = geschuetzt[stationsno]
    preci = df_new["PRECIP"].to_list()
    rskf = df_new["RSKF"].to_list()
    datum = df_new["MESS_DATUM"].to_list()
    meantemp = df_new["TEMP_AVE"]
    rainfall = []
    snowfall = []

    for day in range(len(preci)):
        if math.isnan(rskf[day]):
            rskf_day = 4
        else:
            rskf_day = int(rskf[day])
        
        # kein Niederschlag
        if rskf_day == 0:
            snowfall.append(0)
            rainfall.append(0)
        # Schnee
        elif rskf_day == 7:
            epsilon = 0.82
            b = koeff_b[geschuetztheit][3]
            p_corr = preci[day]+b*preci[day]**epsilon
            snowfall.append(p_corr)
            rainfall.append(0)
        # Mischniederschlag
        elif rskf_day == 8:
            epsilon = 0.55
            b = koeff_b[geschuetztheit][4]
            p_corr = preci[day]+b*preci[day]**epsilon
            rainfall.append(p_corr/2)
            snowfall.append(p_corr/2)
        # Regen
        elif rskf_day == 1 or rskf_day == 6:
            dt = datum[day]
            # DJF
            if dt.month in [12,1,2]:
                epsilon =  0.46
                b = koeff_b[geschuetztheit][1]
                p_corr = preci[day]+b*preci[day]**epsilon
            # JJA
            elif dt.month in [6,7,8]:
                epsilon = 0.38    
                b = koeff_b[geschuetztheit][0]
                p_corr = preci[day]+b*preci[day]**epsilon
            # MAM, SON
            else:
                epsilon = 0.42
                b = koeff_b[geschuetztheit][2]
                p_corr = preci[day]+b*preci[day]**epsilon
            rainfall.append(p_corr)
            snowfall.append(0)
        # not known 
        elif rskf_day == 4 or rskf_day == 9:
            if meantemp[day] < -1:  # Schnee
                epsilon = 0.82
                b = koeff_b[geschuetztheit][3]
                p_corr = preci[day]+b*preci[day]**epsilon
                snowfall.append(p_corr)
                rainfall.append(0)
                rskf[day] = 7 # add new value
            elif -1 <= meantemp[day] <= 1: # Mischniederschlag
                epsilon = 0.55
                b = koeff_b[geschuetztheit][4]
                p_corr = preci[day]+b*preci[day]**epsilon
                rainfall.append(p_corr/2)
                snowfall.append(p_corr/2)
                rskf[day] = 8 # add new value
            else: # Regen
                dt = datum[day]
                # DJF
                if dt.month in [12,1,2]:
                    epsilon =  0.46
                    b = koeff_b[geschuetztheit][1]
                    p_corr = preci[day]+b*preci[day]**epsilon
                # JJA
                elif dt.month in [6,7,8]:
                    epsilon = 0.38    
                    b = koeff_b[geschuetztheit][0]
                    p_corr = preci[day]+b*preci[day]**epsilon
                # MAM, SON
                else:
                    epsilon = 0.42
                    b = koeff_b[geschuetztheit][2]
                    p_corr = preci[day]+b*preci[day]**epsilon
                rainfall.append(p_corr)
                snowfall.append(0)
                rskf[day] = 1 # add new value
        else:
            print(stationsno, day, type(rskf[day]), "No RSKF found.")

    # Round precipitation values
    rainfall = [round(x,1) for x in rainfall]
    snowfall = [round(x,1) for x in snowfall]
    df_new["RAINFALL"] = rainfall
    df_new["SNOWFALL"] = snowfall

    # remove columns not used for rvt file    
    df_new = df_new.drop(["MESS_DATUM"], axis=1)
    df_new = df_new.drop(["RSKF"], axis=1)
    df_new = df_new.drop(["PRECIP"], axis=1)
    return df_new


def split_precip(df):
    """ 
    Split precipitation into rain/snow.
    """
    preci = df["PRECIP"].to_list()
    meantemp = df["TEMP_AVE"]
    rainfall = []
    snowfall = []
    for day in range(len(preci)):
        if meantemp[day] < -1:  # Schnee
            snowfall.append(preci[day])
            rainfall.append(0)
        elif -1 <= meantemp[day] <= 1: # Mischniederschlag
            rainfall.append(preci[day]/2)
            snowfall.append(preci[day]/2)
        else: # Regen
            rainfall.append(preci[day])
            snowfall.append(0)
    df["RAINFALL"] = [round(x,1) for x in rainfall]
    df["SNOWFALL"] = [round(x,1) for x in snowfall]
    df = df.drop(["MESS_DATUM"], axis=1)
    df = df.drop(["PRECIP"], axis=1)
    return df