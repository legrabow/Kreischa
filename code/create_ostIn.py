from datetime import datetime
import pandas as pd
start = datetime.strptime("01.10.2002","%d.%m.%Y")
end = datetime.strptime("30.09.2004","%d.%m.%Y")
pathToAbfluss = "/home/grabow/git/Kreischa/data/Abfluss_Kreischa_2000_2020.csv"
pathForOstIn = "/home/grabow/ostrich/ravenApplication/ostIn.txt"

lines = []

# essential variables
lines.append("# essential variables")
lines.append("ProgramType ParticleSwarm")
lines.append("ModelExecutable /home/grabow/raven/bin/Raven.exe")
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
lines.append("Kal_POROSITY 0.49732 0.0 1.0 none none none free")
lines.append("Kal_FIELD_CAPACITY 0.11777 0.0 1.0 none none none free")
lines.append("Kal_SAT_WILT 0.0 0.0 1.0 none none none free")
lines.append("Kal_HBV_BETA 0.57569 0.0 10.0 none none none free")  #Check!
lines.append("Kal_MAX_CAP_RISE_RATE 1.1216 0.0 350.0 none none none free")
lines.append("Kal_MAX_PERC_RATE 0.0 0.01 1000.0 none none none free")
lines.append("Kal_BASEFLOW_COEFF 0.05 0.0 1.0 none none none free")
lines.append("Kal_BASEFLOW_N 1.0 1 10.0 none none none free")
lines.append("EndParams")

# observation
df = pd.read_csv(pathToAbfluss, decimal=",", header=2)
df['Datum'] = pd.to_datetime(df['Datum'], format='%d.%m.%Y')
calibrationDf = df[(df['Datum'] <= end) & (df['Datum'] >= start)]

lines.append("BeginObservations")
rowNmb = 1
for index, row in calibrationDf.iterrows():
    subline = []
    subline.append("Date" + row["Datum"].strftime("%Y%m%d"))
    subline.append(str(row["Durchfluss"]))
    subline.append("1.00")
    subline.append(pathToAbfluss)
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


with open(pathForOstIn, 'w') as f:
    f.writelines("%s\n" % l for l in lines)
