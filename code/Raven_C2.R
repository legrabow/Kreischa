## setting the soilclass parameters
setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files_c2")


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
                        1, 6 # depth fix 3
), 2, 21)

# colnames(Param_Range) <- Param_Name
rownames(Param_Range) <- c("min", "max")
cali3_Raven(Param_Range["min",], Model_Name, n_Warmup, Q_Observ)

#### calibrate parameter set with DDS ####
fit_dds <- dds(cali3_Raven, 
               Param_Range["min",], 
               Param_Range["max",], 
               # x_Init = unlist(param_Cali2[order(gof_Cali2$V1)[1],]),
               max_iter = 500, 
               Model_Name = Model_Name,
               n_Warmup = n_Warmup,
               Q_Observ = Q_Observ,
               fct_gof = rmse)
gof_Cali_C2 <- read.table("log_gof.txt")
param_Cali_C2 <- read.table("log_param.txt")

best_param_cali_C2 <- unlist(param_Cali3[order(param_Cali_C2$V1)[1],])

best_gof_cali3 <- cali3_Raven(best_param_cali3, Model_Name, n_Warmup, Q_Observ)
Q_Raven_C2 <- read.csv("cali_Hydrographs.csv")



ggplot() +
  geom_line(aes(1462:3288, Q_Observ), color = "blue") + 
geom_line(aes(1462:3288, Q_Raven2$KS_53719235..m3.s.[-(1:n_Warmup)]), color = "yellow") +
  geom_line(aes(1462:3288, Q_Raven3$KS_53719235..m3.s.[-(1:n_Warmup)]), color = "red")

