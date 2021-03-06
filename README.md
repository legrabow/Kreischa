# Kreischa
Modelling the catchment area Kreischa (historical and future scenarios) with the hydrological model Raven as part of the lecture MHYD05 "Einzugsgebietsmodellierung" at TU Dresden.


# Content
**code** contains python/R code for creating Raven and Ostrich input files and hydrological response units (HRU) as well as plotting functions for the model output.  
**data** contains geographical data (shp's) and soil data.   
**model_files*** contains Raven input files and/or results (historical run: 2001 - 2019, future run: 2006 - 2100).  
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
datetime 4.3, fiona 1.8.20, geopandas 0.10.2, matplotlib 3.5.1, numpy 1.22.0, pandas 1.3.5, proplot 0.9.5, pymannkendall 1.4.2, rasterio 1.2.10, richdem 0.3.4, scipy 1.7.3, shapely 1.8.0   
#### R
- `raster 3.5-2` and `rgeos 0.5-9` for geo-data
- `tidyverse 1.3.1` for data processig and plot, 
- `patchwork 1.1.1` for figures layout
