from datetime import datetime
import pandas as pd
startWarmUp = datetime.strptime("01.01.2001","%d.%m.%Y")
startCalibration = datetime.strptime("01.01.2004","%d.%m.%Y")
endCalibration = datetime.strptime("31.12.2008","%d.%m.%Y")
pathToAbfluss = "/home/grabow/git/Kreischa/data/Abfluss_Kreischa_2000_2020.csv"
pathToAbflussRaven = "/home/grabow/raven/bin/run1_Hydrographs.csv"
pathForOstIn = "/home/grabow/ostrich/ravenApplication/ostIn.txt"

lines = []

# essential variables
lines.append("# essential variables")
lines.append("ProgramType Levenberg-Marquardt")
lines.append("ModelExecutable /home/grabow/raven/bin/callRaven.sh")
lines.append("ObjectiveFunction wsse")

# optional variables
lines.append("# optional variables")
lines.append("RandomSeed 123")

# file pairs
lines.append("BeginFilePairs")
lines.append("template.rvp ; /home/grabow/raven/bin/Kreischa.rvp")
lines.append("EndFilePairs")

# parameters
lines.append("BeginParams")
lines.append("Kal_POROSITY 0.49732 0.1 0.9 none none none free")
lines.append("Kal_FIELD_CAPACITY 0.11777 0.001 0.999 none none none free")
lines.append("Kal_SAT_WILT 0.0 0.001 0.999 none none none free")
lines.append("Kal_HBV_BETA 0.57569 0.001 10.0 none none none free")  #Check!
lines.append("Kal_MAX_CAP_RISE_RATE 1.1216 0.001 5.0 none none none free")
lines.append("Kal_MAX_PERC_RATE 0.0 0.001 1000.0 none none none free")
lines.append("Kal_BASEFLOW_COEFF 0.05 0.001 0.999 none none none free")
lines.append("Kal_BASEFLOW_N 1.0 1.0 10.0 none none none free")
lines.append("Kal_SAI_HT_RATIO 0.0 0.001 0.999")
lines.append("Kal_MAX_CAPACITY 16.2593 0.001 2.999")
lines.append("Kal_MAX_SNOW_CAPACITY 6.6763 0.001 2.999")
lines.append("Kal_RAIN_ICEPT_FACT 0.05 0.003 0.008")
lines.append("Kal_SNOW_ICEPT_FACT 0.05 0.002 0.006")
lines.append("Kal_RAIN_ICEPT_PCT 0.05 0.001 0.999")
lines.append("Kal_SNOW_ICEPT_PCT 0.05 0.001 0.999")
lines.append("Kal_MELT_FACTOR 3.1339 1 2")
lines.append("Kal_MIN_MELT_FACTOR 1.3036 1.5 3.5")
lines.append("Kal_HBV_MELT_FOR_CORR 1.0 0.5 0.99")
lines.append("Kal_REFREEZE_FACTOR 1.0 0.001 0.999")
lines.append("Kal_HBV_MELT_ASP_CORR 0.65836 0.5 0.99")
lines.append("EndParams")

# observation
df = pd.read_csv(pathToAbfluss, decimal=",", header=2)
df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
calibrationDf = df[(df['Datum'] <= endCalibration) & (df['Datum'] >= startCalibration)]

lines.append("BeginObservations")
shift = startCalibration - startWarmUp
rowNmb = 1 + shift.days
for index, row in calibrationDf.iterrows():
    subline = []
    subline.append("Date" + row["Datum"].strftime("%Y%m%d"))
    subline.append(str(row["Durchfluss"]))
    subline.append("1.00")
    subline.append(pathToAbflussRaven)
    subline.append(";")
    subline.append("OST_NULL")
    subline.append(str(rowNmb))
    subline.append("5")
    subline.append("\',\'")
    subline.append("no")
    subline.append("mw")
    lineStr = ' '.join(subline)
    lines.append(lineStr)
    rowNmb = rowNmb + 1
# name val wgt filenamee ; keyword line col tok aug? group
lines.append("EndObservations")

# add glm algorithm config
lines.append("BeginLevMar")
lines.append("MaxIterations: 50")
lines.append("EndLevMar")

# add math and start
lines.append("BeginMathAndStats")
lines.append("DiffType best-fit")
lines.append("AllStats")
lines.append("Sensitivity")
lines.append("EndMathAndStats")

with open(pathForOstIn, 'w') as f:
    f.writelines("%s\n" % l for l in lines)
