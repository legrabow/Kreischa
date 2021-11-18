# Builds spatial subsets based on the land use and soil maps
import geopandas as gpd
from geopandas.tools import overlay
pathToLanduse = "/home/grabow/Dropbox/Daten_Kreischa/Landnutzung/Lfulg/Daten/btlnk_flaechen.shp"
pathToSoil = "/home/grabow/Dropbox/Uni/Einzugsgebietsmodellierung/Boden/DATEN/BK50.shp"


## prepare land use layer
landuse = gpd.read_file(pathToLanduse)
levelOfDetail = "HG" # HG, UG or Bestand

if levelOfDetail == "HG":
    uniqueColumn = landuse.HG.astype(str)
if levelOfDetail == "UG":
    uniqueColumn = landuse.HG.astype(str) + landuse.UG.astype(str)
if levelOfDetail == "Bestand":
    uniqueColumn = landuse.HG.astype(str) + landuse.UG.astype(str) + landuse.BESTAND.astype(str)
    
landuse["uniqueColumn"] = uniqueColumn
landuseReduced = landuse.dissolve(by = "uniqueColumn")

## prepare soil layer
soil = gpd.read_file(pathToSoil)
soilReduced = soil.dissolve(by = "BOTYP")

## create HRUs
hru = soilReduced.overlay(landuseReduced, how='union')
hru.to_file("/home/grabow/Dropbox/Daten_Kreischa/Hydrotope/hru.shp")
