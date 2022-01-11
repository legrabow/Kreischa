# FIXME: Import issues with mask module

# WARNING: HRUs and DEM must have the same crs. please check beforehand!

import fiona
from fiona import transform
import numpy as np
import rasterio
from rasterio import mask as msk
from shapely.geometry import shape, Polygon
import richdem as rd

def clean_hruDict(hruDict):
    hruDictClean = {}
    for hruID in hruDict:
        infoDict = hruDict[hruID]
        # check for nan and None types
        anyNAs = []
        for val in infoDict.values():
            try:
                b1 = np.isnan(val)
            except TypeError:
                b1 = False
            b2 = not bool(val)
            bMerged = b1 or b2
            anyNAs.append(bMerged)
        if not np.any(anyNAs):
            hruDictClean[hruID] = infoDict
    return hruDictClean

def get_box(tiffArray, wholeArea, increaseBy = 0):
    # NO USE

    xArrayOld, yArrayOld = np.where((~np.isnan(tiffArray)))
    xMax = np.max(xArrayOld) + increaseBy + 1
    xMin = np.min(xArrayOld) - increaseBy
    yMax = np.max(yArrayOld) + increaseBy + 1
    yMin = np.min(yArrayOld) - increaseBy

    xArrayNew = np.arange(xMin, xMax, 1)
    yArrayNew = np.arange(yMin, yMax, 1)

    subTiffArray = wholeArea[np.ix_(xArrayNew, yArrayNew)]

    return subTiffArray


def get_elevation(tiffArray):
    elevation = np.nanmean(tiffArray)
    return elevation

def get_area(subShape):
    pol = Polygon(subShape["coordinates"][0])
    # get area in km^2
    area = pol.area * 10**(-6)
    centroidPoint = pol.centroid
    return area, centroidPoint

def get_polgyons(pathToShapes):
    sbbDict = {}
    with fiona.open(pathToShapes, "r") as shfSbb:
        for sbb in shfSbb:
            pol = Polygon(sbb["geometry"]["coordinates"][0])
            name = int(sbb["properties"]["OBJECTID"])
            sbbDict[name] = pol
    return sbbDict

def convert_to_standard(tiffArray, metaInfo):
    # assign np.nan to no datas
    tiffArray = tiffArray.astype("float")
    tiffArray[tiffArray == metaInfo["nodata"]] = np.nan
    # convert to units of meter and make it 2D
    tiffArray = tiffArray[0,:,:] / 100

    return tiffArray

def main(pathToHRUs, pathToDEM, pathToSubbasins, pathForSlope, pathForAspect):
    with rasterio.open(pathToDEM) as src:
        metaInfo = src.meta
        wholeArea = src.read()

        wholeArea = convert_to_standard(wholeArea, metaInfo)

        # prepare richdem array
        rdArray  = rd.rdarray(wholeArea, no_data=np.nan)

        # get polygon dicitonary of the subbasins
        sbbDict = get_polgyons(pathToSubbasins)

        # create slope layer in deg
        slope = rd.TerrainAttribute(rdArray, attrib='slope_degrees')
        with rasterio.open(pathForSlope, 'w', **metaInfo) as srcSlope:
            srcSlope.write(slope, 1)

        # create aspect in deg from north ? FIXME
        aspect = rd.TerrainAttribute(rdArray, attrib='aspect')
        with rasterio.open(pathForAspect, 'w', **metaInfo) as srcAspect:
            srcAspect.write(aspect, 1)

        # open slope as read
        with rasterio.open(pathForSlope) as srcSlope:
            # open aspect as read
            with rasterio.open(pathForAspect) as srcAspect:

                hruDict = {}
                counter = 0
                # open HRU shape file and iterate for each hrus
                with fiona.open(pathToHRUs, "r") as shf:
                    hrusCrs = shf.crs["init"]
                    for hru in shf:
                        infoDict = {}
                        shapefileObj = hru["geometry"]

                        # get the area and lat / lon of the centroid point for the HRU
                        area, centroidPoint = get_area(shapefileObj)
                        lon = centroidPoint.x
                        lat = centroidPoint.y
                        lonDeg, latDeg = transform.transform(hrusCrs, "epsg:4326", [lon], [lat])
                        infoDict["lon"] = lonDeg[0]
                        infoDict["lat"] = latDeg[0]
                        infoDict["area"] = area

                        # find subbasin of the HRU
                        subbasinID = None
                        for name in sbbDict:
                            pol = sbbDict[name]
                            if pol.contains(centroidPoint):
                                subbasinID = int(name)
                                break
                        if subbasinID:
                            infoDict["subbasinID"] = subbasinID
                        else:
                            continue

                        # get DEM mask for HRU and get the mean elevation
                        outputTiff, outputTransform = msk.mask(src, [shapefileObj], crop=True)
                        outputTiff = convert_to_standard(outputTiff, metaInfo)
                        elevation = get_elevation(outputTiff)
                        infoDict["elevation"] = elevation

                        # get slope and aspect of the centroid point
                        slopeGen = srcSlope.sample([(lon, lat)])
                        slopePoint = [point for point in slopeGen]
                        aspectgen = srcAspect.sample([(lon, lat)])
                        aspectPoint = [point for point in aspectgen]
                        infoDict["slopePoint"] = slopePoint[0][0]
                        infoDict["aspectPoint"] = aspectPoint[0][0]

                        # add land use class
                        infoDict["landuse"] = "LV_" + str(hru["properties"]["unique"])
                        # add soil class
                        try:
                            infoDict["soil"] = "S_" + str(int(hru["properties"]["LEG_NR_1"]))
                        except TypeError:
                            continue

                        hruID = str(hru["properties"]["level_0"]) + str(hru["properties"]["level_0"])
                        hruDict[hruID] = infoDict
    return hruDict
