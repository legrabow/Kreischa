setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_v1")
system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
Q_Raven_V1 <- read.csv("cali_Hydrographs.csv")
setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_v2")
system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
Q_Raven_V2 <- read.csv("cali_Hydrographs.csv")
setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_v3")
system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
Q_Raven_V3 <- read.csv("cali_Hydrographs.csv")

index_start_raven1 <- which(Q_Raven_V1$date == "2009-01-01")+1 #1462
index_end_raven1 <- which(Q_Raven_V1$date == "2013-12-31")+1 #3288
index_start_raven2 <- which(Q_Raven_V1$date == "2015-01-01")+1 #1462
index_end_raven2 <- which(Q_Raven_V1$date == "2019-12-31")+1 #3288

Q_Raven_V11 <- Q_Raven_V1$KS_53719235..m3.s.[index_start_raven1:index_end_raven1]
Q_Raven_V21 <- Q_Raven_V2$KS_53719235..m3.s.[index_start_raven1:index_end_raven1]
Q_Raven_V31 <- Q_Raven_V3$KS_53719235..m3.s.[index_start_raven1:index_end_raven1]
Q_Raven_V12 <- Q_Raven_V1$KS_53719235..m3.s.[index_start_raven2:index_end_raven2]
Q_Raven_V22 <- Q_Raven_V2$KS_53719235..m3.s.[index_start_raven2:index_end_raven2]
Q_Raven_V32 <- Q_Raven_V3$KS_53719235..m3.s.[index_start_raven2:index_end_raven2]

index_start_V1 <- which(Q_Kreischa$Datum == "01.01.2009") #1462
index_end_V1 <- which(Q_Kreischa$Datum == "31.12.2013") #3288
Q_Kreischa_V1 <- Q_Kreischa$Durchfluss[index_start_V1:index_end_V1]
index_start_V2 <- which(Q_Kreischa$Datum == "01.01.2015") #1462
index_end_V2 <- which(Q_Kreischa$Datum == "31.12.2019") #3288
Q_Kreischa_V2 <- Q_Kreischa$Durchfluss[index_start_V2:index_end_V2]


NSE_V11 <- NSE(Q_Raven_V11, Q_Kreischa_V1)
NSE_V21 <- NSE(Q_Raven_V21, Q_Kreischa_V1)
NSE_V31 <- NSE(Q_Raven_V31, Q_Kreischa_V1)
NSE_V12 <- NSE(Q_Raven_V12, Q_Kreischa_V2)
NSE_V22 <- NSE(Q_Raven_V22, Q_Kreischa_V2)
NSE_V32 <- NSE(Q_Raven_V32, Q_Kreischa_V2)

rmse_V11 <- rmse(Q_Raven_V11, Q_Kreischa_V1)
rmse_V21 <- rmse(Q_Raven_V21, Q_Kreischa_V1)
rmse_V31 <- rmse(Q_Raven_V31, Q_Kreischa_V1)
rmse_V12 <- rmse(Q_Raven_V12, Q_Kreischa_V2)
rmse_V22 <- rmse(Q_Raven_V22, Q_Kreischa_V2)
rmse_V32 <- rmse(Q_Raven_V32, Q_Kreischa_V2)



## Homogenity ####
setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_v1")
meteo_991_lines <- readLines("dwd_00991.rvt") 
meteo_991 <- read.table(text = meteo_991_lines[5:7309])
names(meteo_991) <- c("WIND_VEL", "CLOUD_COVER", "AIR_PRES", "TEMP_AVE", 
                      "REL_HUMIDITY", "TEMP_MAX", "TEMP_MIN", "RAINFALL", "SNOWFALL")
index_start_meteo_c <- which(Q_Raven_V1$date == "2004-01-01") #1462
index_end_meteo_c <- which(Q_Raven_V1$date == "2008-12-30") #3288
index_start_meteo_v1 <- which(Q_Raven_V1$date == "2009-01-01") #1462
index_end_meteo_v1 <- which(Q_Raven_V1$date == "2013-12-31") #3288
index_start_meteo_v2 <- which(Q_Raven_V1$date == "2015-01-01") #1462
index_end_meteo_v2 <- which(Q_Raven_V1$date == "2019-12-31") #3288

