# FIXME: Import issues with mask module

# WARNING: HRUs and DEM must have the same crs. please check beforehand!

import fiona
import numpy as np
import rasterio
from rasterio import mask as msk
from shapely.geometry import shape, Polygon
import richdem as rd

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
    area = pol.area
    centroidPoint = pol.centroid
    return area, centroidPoint

def get_polgyons(pathToShapes):
    sbbDict = {}
    with fiona.open(pathToShapes, "r") as shfSbb:
        for sbb in shfSbb:
            pol = Polygon(sbb["geometry"]["coordinates"][0])
            name = sbb["properties"]["fid"]
            sbbDict[name] = pol
    return sbbDict

def convert_to_standard(tiffArray):
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

        wholeArea = convert_to_standard(wholeArea)

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
                    for hru in shf:
                        infoDict = {}
                        shapefileObj = hru["geometry"]

                        # get DEM mask for HRU and get the mean elevation
                        outputTiff, outputTransform = msk.mask(src, [shapefileObj], crop=True)
                        outputTiff = convert_to_standard(outputTiff)
                        elevation = get_elevation(outputTiff)
                        infoDict["elevation"] = elevation

                        # get the area and lat / lon of the centroid point for the HRU
                        area, centroidPoint = get_area(shapefileObj)
                        lon = centroidPoint.x
                        lat = centroidPoint.y
                        infoDict["lon"] = lon
                        infoDict["lat"] = lat

                        # get slope and aspect of the centroid point
                        slopeGen = srcSlope.sample([(lon, lat)])
                        slopePoint = [point for point in slopeGen]
                        aspectgen = srcAspect.sample([(lon, lat)])
                        aspectPoint = [point for point in aspectgen]
                        infoDict["slopePoint"] = slopePoint[0][0]
                        infoDict["aspectPoint"] = aspectPoint[0][0]

                        # find subbasin of the HRU
                        for name in sbbDict:
                            pol = sbbDict[name]
                            if pol.contains(centroidPoint):
                                subbasinID = int(name)
                                break
                        infoDict["subbasinID"] = subbasinID

                        name = str(hru["properties"]["level_0"]) + str(hru["properties"]["level_0"])
                        hruDict[name] = infoDict
    return hruDict
