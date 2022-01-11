import pandas as pd

import get_hru_infos as ghi

def main(pathForRvh, pathToSubbasinsTable, pathToSubbasinsShape, pathToHRUs, pathToDEM, pathForSlope, pathForAspect):
    lines = []

    ## add preamble
    lines.append("# --------------------------------------------")
    lines.append("# Raven HRU Input file")
    lines.append("# --------------------------------------------")

    ## add SubBasins section
    lines.append(":SubBasins")
    lines.append("  :Attributes   NAME  DOWNSTREAM_ID       PROFILE REACH_LENGTH  GAUGED")
    lines.append("  :Units        none           none          none           km    none")


    subbasins = pd.read_csv(pathToSubbasinsTable)
    nrow = subbasins.shape[0]
    for sbIdx in range(nrow):
        line = []
        # add ID
        sbID = str(subbasins.OBJECTID[sbIdx])
        line.append(sbID)
        # add name
        sbName = "Sub" + sbID
        line.append(sbName)
        # add downstream ID
        downstreamID = str(subbasins.TO[sbIdx])
        if downstreamID == "-":
            downstreamID = "[None]"
        line.append(downstreamID)
        # add profile
        profile = "DEFAULT"
        line.append(profile)
        # add reach length
        reachLength = "_AUTO"
        line.append(reachLength)
        # add gauged
        gauged = "0"
        line.append(gauged)

        # merge to one line string
        lineStr = ', '.join(line)
        # add to lines
        lines.append(lineStr)

    lines.append(":EndSubBasins")

    ## add SubBasinProperties section
    """
    lines.append(":SubBasinProperties")
    lines.append("  :Parameters TIME_CONC   TIME_TO_PEAK  TIME_LAG")
    lines.append("  :Units             d               d         d")
    lines.append(":EndSubBasinProperties")
    for sbIdx in range(nrow):
        line = []
        # add ID
        sbID = str(subbasins.OBJECTID[sbIdx])
        line.append(sbID)
        # add time_conc
        line.append("1.27")
        # add time_to_peak
        line.append("0.75")
        # add time_lag
        line.append("0")
        # merge to one line string
        lineStr = ', '.join(line)
        # add to lines
        lines.append(lineStr)
    """
    ## add HRUs section
    lines.append(":HRUs")
    lines.append("  :Attributes AREA ELEVATION  LATITUDE  LONGITUDE   BASIN_ID  LAND_USE_CLASS  VEG_CLASS   SOIL_PROFILE  AQUIFER_PROFILE   TERRAIN_CLASS   SLOPE   ASPECT")
    lines.append("  :Units       km2         m       deg        deg       none            none       none           none             none            none     deg      deg")

    hruDict = ghi.main(pathToHRUs, pathToDEM, pathToSubbasinsShape, pathForSlope, pathForAspect)
    hruDictCleaned = ghi.clean_hruDict(hruDict)
    for hruID in hruDictCleaned:
        infoDict = hruDictCleaned[hruID]
        line = []
        # add ID
        line.append(str(hruID))
        # add area
        line.append(str(infoDict["area"]))
        # add elevation
        line.append(str(infoDict["elevation"]))
        # add lat
        line.append(str(infoDict["lat"]))
        # add lon
        line.append(str(infoDict["lon"]))
        # add basin ID
        line.append(str(infoDict["subbasinID"]))
        # add land use
        line.append(str(infoDict["landuse"]))
        # add veg class
        line.append(str(infoDict["landuse"]))
        # add soil profile
        line.append(str(infoDict["soil"]))
        # add aquifer profile
        line.append("[None]")
        # add terrain class
        line.append("[None]")
        # add slope
        line.append(str(infoDict["slopePoint"]))
        # add aspect
        line.append(str(infoDict["aspectPoint"]))

        # merge to one line string
        lineStr = ', '.join(line)
        # add to lines
        lines.append(lineStr)

    lines.append(":EndHRUs")

    with open(pathForRvh, 'w') as f:
        f.writelines("%s\n" % l for l in lines)
