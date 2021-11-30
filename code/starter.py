import create_rvh as crvh


pathToSubbasinsTable = "/home/grabow/Dropbox/Daten_Kreischa/Hydrotope/subbasinsInterconnection.csv"
pathToHRUs = "/home/grabow/Dropbox/Daten_Kreischa/Hydrotope/hru.shp"
pathToDEM = "/home/grabow/Dropbox/Daten_Kreischa/DGM/Kreischa_DGM.tif"
pathToSubbasinsShape = "/home/grabow/Dropbox/Daten_Kreischa/Gesamtgebiet/Kreischa_TeilEZG_Arbeitsstand.shp"

pathForSlope = "/home/grabow/slope.tif"
pathForAspect = "/home/grabow/aspect.tif"
pathForRvh = "/home/grabow/Documents/test2.rvh"

crvh.main(pathForRvh, pathToSubbasinsTable, pathToSubbasinsShape, pathToHRUs, pathToDEM, pathForSlope, pathForAspect)
