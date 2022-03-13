import os
import pandas as pd
import numpy as np
import subprocess

def change_rvtfile(inputFile, outputFile, subscales):
    with open(inputFile) as fo:
        totalLines = fo.readlines()
        newTotalLines = totalLines.copy()
        endLine = len(totalLines)
        headerLine = totalLines[2]

        for idx in range(4, endLine -1):
            line = totalLines[idx].replace("\t\t","")
            line = line.replace(" \n","")
            lineNP = np.array(line.split(" "))
            lineNP = lineNP.astype(float)
            newLineNP = lineNP.copy()
            newLineNP[:] = np.nan
            if any(np.isnan(lineNP)):
                raise Exception()
            for scIdx,n in enumerate(lineNP):
                error = np.random.normal(loc=0.0, scale=subscales[scIdx]*abs(n)/100.0)
                result = n + error
                result = np.round(result, 4)
                if result < 0 and scIdx in [0,1,2,4,7,8,9]:
                    result = 0
                newLineNP[scIdx] = result
            newLine = " ".join(newLineNP.astype(str))
            newLine = f"\t\t{newLine} \n"
            newTotalLines[idx] = newLine
    with open(outputFile, 'w') as fo:
        fo.writelines(newTotalLines)
        
def change_discharge(inputFile, outputFile, errorOutput):
    with open(inputFile) as fo:
        totalLines = fo.readlines()
        newTotalLines = totalLines.copy()
        for idx in range(32, 1859):
            line = totalLines[idx]
            lineNP = np.array(line.split(" "))
            n = lineNP[1].astype(float)
            error = np.random.normal(loc=0.0, scale=errorOutput*abs(n)/100.0)
            result = n + error
            result = np.round(result, 4)
            lineNP[1] = result.astype(str)
            newLine = " ".join(lineNP)
            newTotalLines[idx] = newLine
    with open(outputFile, 'w') as fo:
        fo.writelines(newTotalLines)
        
def change_seed(inputFile, outputFile, sim):
    with open(inputFile) as fo:
        totalLines = fo.readlines()
        newTotalLines = totalLines.copy()
        seedLine = f"RandomSeed {sim}\n"
        newTotalLines[5] = seedLine
    with open(outputFile, 'w') as fo:
        fo.writelines(newTotalLines)
        
def read_output(OstOutputFile, sim):
    with open(OstOutputFile) as fo:
        totalLines = fo.readlines()
        startidx = [idx for idx,l in enumerate(totalLines) if "Optimal Parameter Set" in l]

    out = pd.read_csv(OstOutputFile, skiprows=startidx[0]+1, nrows=21,index_col=0, header=None, sep=":")
    out.columns = [str(sim)]
    return out

# directory of uncorrupted rvt files
rvtDir = "./rvt_backup"

# target directory of Ostrich
ostrichDir = "."

# ostIn.txt backup file 
ostin = "./ostIn_TEMPLATE.txt"

# stanadard deviation factor for normal distribution in percentage
errorInput = {
    "WIND_VEL":5.0,
    "CLOUD_COVER":5.0,
    "AIR_PRES":5.0,
    "TEMP_AVE":5.0,
    "REL_HUMIDITY":5.0,
    "TEMP_MAX":5.0,
    "TEMP_MIN":5.0,
    "RAINFALL":5.0,
    "SNOWFALL":5.0,
    "SHORTWAVE":5.0
}

# stanadard deviation factor for normal distribution in percentage
errorOutput = 5.0

# number of trials
trials = 3
# shift number for directory applied
shift = 0

parameterResults = []
rvtFiles = os.listdir(rvtDir)
OstOutputFile = os.path.join(ostrichDir, "OstOutput0.txt")
ostInFile = os.path.join(ostrichDir, "ostIn.txt")
scales = [errorInput["WIND_VEL"],errorInput["CLOUD_COVER"], errorInput["AIR_PRES"], \
          errorInput["TEMP_AVE"], errorInput["REL_HUMIDITY"], errorInput["TEMP_MAX"], \
          errorInput["TEMP_MIN"], errorInput["RAINFALL"], errorInput["SNOWFALL"],\
          errorInput["SHORTWAVE"]]

for sim in range(shift, shift + trials):
    print(f"Trial {sim}")
    print("############### Adjust input files #######################")
    for f in rvtFiles:
        rvtinputFile = os.path.join(rvtDir, f)
        rvtoutputFile = os.path.join(ostrichDir, f)
        change_rvtfile(rvtinputFile, rvtoutputFile, scales)
    
    change_discharge(ostin, ostInFile, errorOutput)
    change_seed(ostInFile, ostInFile, sim)
    print("############### Call Ostrich #######################")
    try:
        subprocess.call(["./callOstrich.sh"])
    except CalledProcessError:
        print("Error occured")
        continue
    df = read_output(OstOutputFile, sim)
    os.remove(OstOutputFile)
    os.remove(ostInFile)
    fName = "trial_" + str(sim) + "_parameters.csv"
    df.to_csv(fName)
