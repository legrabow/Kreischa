cali_Raven <- function(Param_, Model_Name, n_Warmup, Q_Observ, fct_gof = NSE) {
  rvp_File <- readLines(paste0(Model_Name, ".rvp"))
  rvp_File[grep(":SoilParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[1:8], collapse = " "))
  rvp_File[grep(":VegetationParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[9:15], collapse = " "))
  rvp_File[grep(":LandUseParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[16:20], collapse = " "))
  writeLines(rvp_File, paste0(Model_Name, ".rvp"))
  system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
  Q_Raven <- read.csv("cali_Hydrographs.csv")
  gof_ <- fct_gof(Q_Raven$KS_53719235..m3.s.[-(1:n_Warmup)], Q_Observ)
  write(gof_, "log_gof.txt", append = TRUE)
  write(paste(Param_, collapse = " "), "log_param.txt", append = TRUE)
  return(gof_)
}


cali_Raven_sensi <- function(Param_Sensi, Param_, Param_Index, Model_Name, n_Warmup, Q_Observ, fct_gof = NSE) {
  Param_[Param_Index] <- Param_Sensi
  
  rvp_File <- readLines(paste0(Model_Name, ".rvp"))
  rvp_File[grep(":SoilParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[1:8], collapse = " "))
  rvp_File[grep(":VegetationParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[9:15], collapse = " "))
  rvp_File[grep(":LandUseParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[16:20], collapse = " "))
  writeLines(rvp_File, paste0(Model_Name, ".rvp"))
  system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
  Q_Raven <- read.csv("cali_Hydrographs.csv")
  gof_ <- fct_gof(Q_Raven$KS_53719235..m3.s.[-(1:n_Warmup)], Q_Observ)
  write(gof_, "log_gof.txt", append = TRUE)
  write(paste(Param_, collapse = " "), "log_param.txt", append = TRUE)
  return(gof_)
}








cali2_Raven <- function(Param_, Model_Name, n_Warmup, Q_Observ, fct_gof = NSE, 
                        soil_profil_write = soil_profil, soil_param_write = soil_param_all) {
  # Param_ <- unlist(Param_)
  # soil_profil_write <- soil_profil
  soil_profil_write[,4] <- soil_profil_write[,4] * Param_[10]
  soil_profil_write[,6] <- soil_profil_write[,6] * Param_[11]
  soil_profil_write[,8] <- soil_profil_write[,8] * Param_[12]
  # soil_param_write <- soil_param_all
  soil_param_write[2:7, c(2,3,8)] <- rep(Param_[c(1, 4, 7)], each = 6)
  soil_param_write[8:20, c(2,3,8)] <- rep(Param_[c(2, 5, 8)], each = 13)
  soil_param_write[21:26, c(2,3,8)] <- rep(Param_[c(3, 6, 9)], each = 6)
  
  rvp_File <- readLines(paste0(Model_Name, "_ori.rvp"))
  write(rvp_File[1:34], paste0(Model_Name, ".rvp"))
  write.table(soil_profil_write, paste0(Model_Name, ".rvp"), append = T, col.names = F, row.names = F, quote = F)
  write(rvp_File[71:74], paste0(Model_Name, ".rvp"), append = T)
  write.table(soil_param_write, paste0(Model_Name, ".rvp"), append = T, col.names = F, row.names = F)
  write(rvp_File[101:223], paste0(Model_Name, ".rvp"), append = T)

  system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
  Q_Raven <- read.csv("cali_Hydrographs.csv")
  gof_ <- fct_gof(Q_Raven[-(1:n_Warmup),5], Q_Observ)
  write(gof_, "log_gof.txt", append = TRUE)
  write(paste(Param_, collapse = " "), "log_param.txt", append = TRUE)
  return(gof_)
}


cali3_Raven <- function(Param_, Model_Name, n_Warmup, Q_Observ, fct_gof = NSE, 
                        soil_profil_write = soil_profil, soil_param_write = soil_param_all) {
  # Param_ <- unlist(Param_)
  # soil_profil_write <- soil_profil
  soil_profil_write[,4] <- soil_profil_write[,4] * Param_[19]
  soil_profil_write[,6] <- soil_profil_write[,6] * Param_[20]
  soil_profil_write[,8] <- soil_profil_write[,8] * Param_[21]
  # soil_param_write <- soil_param_all
  soil_param_write[2:4, c(2,3,8)] <- rep(Param_[c(1, 7, 13)], each = 3)
  soil_param_write[5:7, c(2,3,8)] <- rep(Param_[c(2, 8, 14)], each = 3)
  soil_param_write[8:11, c(2,3,8)] <- rep(Param_[c(3, 9, 15)], each = 4)
  soil_param_write[12:15, c(2,3,8)] <- rep(Param_[c(4, 10, 16)], each = 4)
  soil_param_write[16:20, c(2,3,8)] <- rep(Param_[c(5, 11, 17)], each = 5)
  soil_param_write[21:26, c(2,3,8)] <- rep(Param_[c(6, 12, 18)], each = 6)
  
  rvp_File <- readLines(paste0(Model_Name, "_ori.rvp"))
  write(rvp_File[1:34], paste0(Model_Name, ".rvp"))
  write.table(soil_profil_write, paste0(Model_Name, ".rvp"), append = T, col.names = F, row.names = F, quote = F)
  write(rvp_File[71:74], paste0(Model_Name, ".rvp"), append = T)
  write.table(soil_param_write, paste0(Model_Name, ".rvp"), append = T, col.names = F, row.names = F)
  write(rvp_File[101:223], paste0(Model_Name, ".rvp"), append = T)
  
  system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
  Q_Raven <- read.csv("cali_Hydrographs.csv")
  gof_ <- fct_gof(Q_Raven[-(1:n_Warmup),5], Q_Observ)
  write(gof_, "log_gof.txt", append = TRUE)
  write(paste(Param_, collapse = " "), "log_param.txt", append = TRUE)
  return(gof_)
}

cali4_Raven <- function(Param_, Model_Name, n_Warmup, Q_Observ, fct_gof = NSE, 
                        soil_profil_write = soil_profil, soil_param_write = soil_param_all) {
  # Param_ <- unlist(Param_)
  # soil_profil_write <- soil_profil
  soil_profil_write[,4] <- soil_profil_write[,4] * Param_[19]
  soil_profil_write[,6] <- soil_profil_write[,6] * Param_[20]
  soil_profil_write[,8] <- soil_profil_write[,8] * Param_[21]
  # soil_param_write <- soil_param_all
  soil_param_write[2:4, c(2,3,8)] <- rep(Param_[c(1, 7, 13)], each = 3)
  soil_param_write[5:7, c(2,3,8)] <- rep(Param_[c(2, 8, 14)], each = 3)
  soil_param_write[8:11, c(2,3,8)] <- rep(Param_[c(3, 9, 15)], each = 4)
  soil_param_write[12:15, c(2,3,8)] <- rep(Param_[c(4, 10, 16)], each = 4)
  soil_param_write[16:20, c(2,3,8)] <- rep(Param_[c(5, 11, 17)], each = 5)
  soil_param_write[21:26, c(2,3,8)] <- rep(Param_[c(6, 12, 18)], each = 6)
  soil_param_write[2:26, c(4:7,9)] <- rep(Param_[22:26], each = 25)
  
  
  rvp_File <- readLines(paste0(Model_Name, "_ori.rvp"))
  rvp_File[grep(":VegetationParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[27:33], collapse = " "))
  rvp_File[grep(":LandUseParameterList", rvp_File)+3] <- paste(" [DEFAULT]", paste(Param_[34:38], collapse = " "))
  write(rvp_File[1:34], paste0(Model_Name, ".rvp"))
  write.table(soil_profil_write, paste0(Model_Name, ".rvp"), append = T, col.names = F, row.names = F, quote = F)
  write(rvp_File[71:74], paste0(Model_Name, ".rvp"), append = T)
  write.table(soil_param_write, paste0(Model_Name, ".rvp"), append = T, col.names = F, row.names = F)
  write(rvp_File[101:223], paste0(Model_Name, ".rvp"), append = T)
  
  system(paste0("Raven.exe ", Model_Name), ignore.stdout = TRUE)
  Q_Raven <- read.csv("cali_Hydrographs.csv")
  gof_ <- fct_gof(Q_Raven[-(1:n_Warmup),5], Q_Observ)
  write(gof_, "log_gof.txt", append = TRUE)
  write(paste(Param_, collapse = " "), "log_param.txt", append = TRUE)
  return(gof_)
}


sensi_index_NSE <- function(vct_NSE) {
  NSE_Quan <- quantile(vct_NSE, c(0.33,0.5,1), na.rm = TRUE)
  return((NSE_Quan[3] - NSE_Quan[1])/(1 - NSE_Quan[2]))
}

