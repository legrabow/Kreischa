import create_hru

pathToLanduse = "/home/grabow/Dropbox/Daten_Kreischa/Landnutzung/Lfulg/Daten/btlnk_flaechen.shp"
pathToSoil = "/home/grabow/Dropbox/Daten_Kreischa/Boden/Daten/Boden.shp"
pathToHru = "/home/grabow/Dropbox/Daten_Kreischa/Hydrotope/hru.shp"
levelOfDetail = "UG"

create_hru.main(pathToLanduse, pathToSoil, pathToHru, levelOfDetail)
