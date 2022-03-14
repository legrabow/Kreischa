## setting the soilclass parameters
setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_c3")


Param_Range <- matrix(c(0.1, 0.9, # POROSITY #1-7
                        0.1, 0.9, # POROSITY #9-20
                        0.1, 0.9, # POROSITY #21-25
                        0.1, 0.9, # POROSITY #1-7
                        0.1, 0.9, # POROSITY #9-20
                        0.1, 0.9, # POROSITY #21-25
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # BASEFLOW_COEFF
                        0.001, 0.999, # BASEFLOW_COEFF
                        0.001, 0.999, # BASEFLOW_COEFF
                        0.001, 0.999, # BASEFLOW_COEFF
                        0.001, 0.999, # BASEFLOW_COEFF
                        0.001, 0.999, # BASEFLOW_COEFF
                        1, 6, # depth fix 1
                        1, 6, # depth fix 2
                        1, 6, # depth fix 3
                        0.001, 0.999, # SAT_WILT 22
                        0.001, 10, # HBV_BETA 23
                        0.001, 5, # MAX_CAP_RISE_RATE 24
                        0.001, 1000, # MAX_PERC_RATE 25
                        1, 10, # BASEFLOW_N 26
                        0.001, 0.999, # SAI_HT_RATIO # vegetation 27
                        0.001, 2.999, # MAX_CAPACITY 28
                        0.001, 2.999, # MAX_SNOW_CAPACITY 29
                        0.003, 0.008, # RAIN_ICEPT_FACT 30
                        0.002, 0.006, # SNOW_ICEPT_FACT 31
                        0.001, 0.999, # RAIN_ICEPT_PCT 32
                        0.001, 0.999, # SNOW_ICEPT_PCT 33
                        1, 2, # MELT_FACTOR # landuse 34
                        1.5, 3.5, # MIN_MELT_FACTOR 35
                        0.5, 0.99, # HBV_MELT_FOR_CORR 36
                        0.001, 0.999, # REFREEZE_FACTOR 37
                        0.5, 0.99 # HBV_MELT_ASP_CORR 38
), 2, 38)

# colnames(Param_Range) <- Param_Name
rownames(Param_Range) <- c("min", "max")
x_Init4 = unlist(c(param_Cali3[order(gof_Cali3$V1)[1],] , param_Cali[order(gof_Cali$V1)[1],-c(1,2,7)]))
cali4_Raven(x_Init4, Model_Name, n_Warmup, Q_Observ)

#### calibrate parameter set with DDS ####
fit_dds <- dds(cali4_Raven, 
               Param_Range["min",], 
               Param_Range["max",], 
               x_Init = x_Init4,
               max_iter = 1000, 
               Model_Name = Model_Name,
               n_Warmup = n_Warmup,
               Q_Observ = Q_Observ,
               fct_gof = rmse)
gof_Cali_C3 <- read.table("log_gof.txt")
param_Cali_C3 <- read.table("log_param.txt")
best_gof_Cali_C3 <- min(gof_Cali_C3)
best_param_cali_C3 <- unlist(param_Cali_C3[order(gof_Cali_C3$V1)[1],])

best_gof_cali_C3 <- cali4_Raven(best_param_cali_C3, Model_Name, n_Warmup, Q_Observ)
Q_Raven_C3 <- read.csv("cali_Hydrographs.csv")



ggplot() +
  geom_line(aes(1462:3288, Q_Observ), color = "blue") + 
  geom_line(aes(1462:3288, Q_Raven2$KS_53719235..m3.s.[-(1:n_Warmup)]), color = "yellow") +
  geom_line(aes(1462:3288, Q_Raven3$KS_53719235..m3.s.[-(1:n_Warmup)]), color = "red")

