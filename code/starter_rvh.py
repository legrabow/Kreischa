import create_rvh as crvh


pathToSubbasinsTable = "/home/grabow/Dropbox/Daten_Kreischa/Hydrotope/subbasinsInterconnection_aoi.csv"
pathToHRUs = "/home/grabow/Dropbox/Daten_Kreischa/Hydrotope/hru.shp"
pathToDEM = "/home/grabow/Dropbox/Daten_Kreischa/DGM/Kreischa_DGM.tif"
pathToSubbasinsShape = "/home/grabow/Dropbox/Daten_Kreischa/Gesamtgebiet/Kreischa_TeilEZG_Arbeitsstand.shp"

pathForSlope = "/home/grabow/Dropbox/Daten_Kreischa/DGM/slope.tif"
pathForAspect = "/home/grabow/Dropbox/Daten_Kreischa/DGM/aspect.tif"
pathForRvh = "/home/grabow/Dropbox/Daten_Kreischa/Model-Files/HG_aufloesung.rvh"

crvh.main(pathForRvh, pathToSubbasinsTable, pathToSubbasinsShape, pathToHRUs, pathToDEM, pathForSlope, pathForAspect)
