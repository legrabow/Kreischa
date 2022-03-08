# Kreischa
Modelling the catchment area Kreischa (historical and future scenarios) with the hydrological model Raven as part of the lecture MHYD05 "Einzugsgebietsmodellierung" at TU Dresden.


# Content
**code** contains python code for creating Raven and Ostrich input files as well as hydrological response units (HRU).  
**data** contains geographical (shp's) and soil data.   
**model_files** contains Raven input files and results for the historical run.  
**model_files_rcp*** contains Raven input files for the future run (2006 - 2100).  
**ostrich** contains utilities and results of parametrization with ostrich.  

# Overview
<img src="workflow.png" alt="workflow" width="900"/>   

# Usage
1. Download and compile the model Raven.
2. Add model_files* into the model's directory.
3. Run model with ```./Raven.exe Kreischa```.

# Data Source
#### 1. historical meteorological data (DWD's open data server)
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/kl/historical/   
https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/daily/solar/
#### 2. climate simulation data (ReKIS: CMIP5\_CanESM2\_EPISODES-2018)
https://rekisviewer.hydro.tu-dresden.de/fdm/ReKISExpert.jsp#menu-5   
#### 3. soil (LfULG)
https://www.boden.sachsen.de/digitale-bodenkarte-1-50-000-19474.html   
#### 4. land use (LfULG)
https://www.natur.sachsen.de/biotoptypen-und-landnutzungskartierung-btlnk-22282.html
#### 5. DEM (GeoSN)
https://www.landesvermessung.sachsen.de/verfugbarkeit-aktualitat-5305.html

# Packages and Dependencies
#### Python
datetime 4.3, fiona, geopandas, matplotlib 3.5.1, numpy 1.22.0, pandas, proplot 0.9.5, pymannkendall 1.4.2, rasterio, richdem, scipy 1.7.3, shapely   
#### R
todo
