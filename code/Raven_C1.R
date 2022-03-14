library(mcga)
library(hydroGOF)
library(ggplot2)
theme_set(theme_bw())
setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_c1")
Param_Name <- c("POROSITY",   "FIELD_CAPACITY", "SAT_WILT", "HBV_BETA", "MAX_CAP_RISE_RATE",  "MAX_PERC_RATE",  "BASEFLOW_COEFF", "BASEFLOW_N",
                "SAI_HT_RATIO", "MAX_CAPACITY", "MAX_SNOW_CAPACITY",  "RAIN_ICEPT_FACT",  "SNOW_ICEPT_FACT",  "RAIN_ICEPT_PCT",   "SNOW_ICEPT_PCT",
                "MELT_FACTOR",  "MIN_MELT_FACTOR",  "HBV_MELT_FOR_CORR",  "REFREEZE_FACTOR",  "HBV_MELT_ASP_CORR")
Param_Range <- matrix(c(0.1, 0.9, # POROSITY #SOil
                        0.001, 0.999, # FIELD_CAPACITY
                        0.001, 0.999, # SAT_WILT
                        0.001, 10, # HBV_BETA
                        0.001, 5, # MAX_CAP_RISE_RATE
                        0.001, 1000, # MAX_PERC_RATE
                        0.001, 0.999, # BASEFLOW_COEFF
                        1, 10, # BASEFLOW_N
                        0.001, 0.999, # SAI_HT_RATIO # vegetation
                        0.001, 2.999, # MAX_CAPACITY
                        0.001, 2.999, # MAX_SNOW_CAPACITY
                        0.003, 0.008, # RAIN_ICEPT_FACT
                        0.002, 0.006, # SNOW_ICEPT_FACT
                        0.001, 0.999, # RAIN_ICEPT_PCT
                        0.001, 0.999, # SNOW_ICEPT_PCT
                        1, 2, # MELT_FACTOR # landuse
                        1.5, 3.5, # MIN_MELT_FACTOR
                        0.5, 0.99, # HBV_MELT_FOR_CORR
                        0.001, 0.999, # REFREEZE_FACTOR
                        0.5, 0.99 # HBV_MELT_ASP_CORR
                        ), 2, length(Param_Name))

colnames(Param_Range) <- Param_Name
rownames(Param_Range) <- c("min", "max")
n_Warmup <- 1096 # 20010101-20031231 + 1

Q_Kreischa <- read.csv("Abfluss_Kreischa_2000_2020.csv", dec = ",") # cali:1462-3288
index_start_Q <- which(Q_Kreischa$Datum == "01.01.2004") #1462
index_end_Q <- which(Q_Kreischa$Datum == "31.12.2008") #3288
Model_Name = "Kreischa"
Q_Observ <- Q_Kreischa$Durchfluss[index_start_Q:index_end_Q]

# fct_gof = rmse
# Param_ = Param_Range["min",]
cali_Raven(Param_Range["min",], Model_Name, n_Warmup, Q_Observ)


#### calibrate parameter set with GA ####
FitGA_Raven_Kreischa <- mcga2(fitness  = cali_Raven,
                min = Param_Range["min",],
                max = Param_Range["max",],
                Model_Name = Model_Name,
                n_Warmup = n_Warmup,
                Q_Observ = Q_Observ,
                popSize =22,
                maxiter =20)
#### calibrate parameter set with DDS ####
fit_dds <- dds(cali_Raven, 
               Param_Range["min",], 
               Param_Range["max",], 
               # x_Init = fit_dds$x_Best,
               max_iter = 500, 
               Model_Name = Model_Name,
               n_Warmup = n_Warmup,
               Q_Observ = Q_Observ,
               fct_gof = rmse)
gof_Cali <- read.table("log_gof.txt")
param_Cali <- read.table("log_param.txt")
best_param_cali1 <- unlist(param_Cali[order(gof_Cali$V1)[1],])
best_gof_cali1 <- cali_Raven(best_param_cali1, Model_Name, n_Warmup, Q_Observ)
Q_Raven_C1 <- read.csv("cali_Hydrographs.csv")

ggplot() +
  geom_line(aes(1462:3288, Q_Raven$KS_53719235..m3.s.[-(1:n_Warmup)]), color = "red") +
  geom_line(aes(1462:3288, Q_Observ), color = "blue")

## test prosity
cali_Raven(c(1, Param_best[-1]), Model_Name, n_Warmup, Q_Observ) ## 0.6694026
 
## results from Leo
## 0.645510855 0.585478509 0.138787700 0.059556605 0.002677506 0.000000000 1.136437724 0.000000000 
## 0.014163207 0.000000000 0.000000000 0.000000000 0.000000000 0.000000000 0.000000000 
## 0.030587043 0.256949414 0.305556506 0.020065601 0.002008974
best_DDS_1821 = c( 8.977376E-01, 2.095629E-01, 2.081462E-01, 9.970507E+00, 5.630787E-01, 2.222113E+01, 7.600429E-02, 9.966000+00, 
                   4.152819E-03, 2.985008E+00, 2.949828E+00, 4.567291E-03, 2.018199E-03, 9.937375E-01, 8.611022E-01, 
                   1.999644E+00, 3.497631E+00, 9.895729E-01, 1.045096E-02, 5.139204E-01)
best_DDS_1821[8] = 10
cali_Raven(best_DDS_1821, Model_Name, n_Warmup, Q_Observ) ## 0.6282315

best_GLM = c(4.977200E-01, 1.177700E-01, 1.000000E-03, 5.756900E-01, 1.121600E+00, 1.000000E-03, 5.000000E-02, 9.966000E+00, 
             1.000000E-03, 2.999000E+00, 2.5000E+00, 8.000000E-03, 6.000000E-03, 5.000000E-02, 5.000000E-02, 
             2.000000E+00, 1.500000E+00, 9.900000E-01, 9.990000E-01, 6.583600E-01)
cali_Raven(best_GLM, Model_Name, n_Warmup, Q_Observ) ## 0.265293
Param_Sensi[8] = 2.5
cali_Raven(Param_Sensi, Model_Name, n_Warmup, Q_Observ)



