## sensitive anlyse ####
n_dis = 20
Dis_Param <- apply(Param_Range, 2, function(Range_) seq(Range_[1], Range_[2],length.out = n_dis))
Param_best <- param_Cali[order(gof_Cali$V1)[1],]

NSE_Sensi <- matrix(NA, n_dis, 20)
Q_Sensi <- matrix(NA, n_dis, 20)
for (i_para in 1:20) {
  Param_Sensi <- Param_best
  for (i_dis in 1:n_dis) {
    Param_Sensi[i_para] <- Dis_Param[i_dis, i_para]
    NSE_Sensi[i_dis, i_para] <- cali_Raven(Param_Sensi, Model_Name, n_Warmup, Q_Observ)
    Q_Raven <- read.csv("cali_Hydrographs.csv")
    Q_Sensi[i_dis, i_para] <- mean(Q_Raven$KS_53719235..m3.s.[-(1:n_Warmup)])
    
  }
}

## Sensitivität Index
sensi_gof <- read.table("log_sensi_gof.txt")
sensi_param <- read.table("log_sensi_param.txt")
SI_NSE <- apply(NSE_Sensi, 2, sensi_index_NSE)
index_Sensi_Param <- which(SI_all > 0.1)
SI_Nearing_NSE <- ((NSE_Sensi[20,] - NSE_Sensi[1,]) / (NSE_Sensi[20,] + NSE_Sensi[1,])) / 
  ((Param_Range[,2] - Param_Range[,1]) / (Param_Range[,2] + Param_Range[,1]))
SI_Nearing_Q <- ((Q_Sensi[20,] - Q_Sensi[1,]) / (Q_Sensi[20,] + Q_Sensi[1,])) / 
  ((Param_Range[,2] - Param_Range[,1]) / (Param_Range[,2] + Param_Range[,1]))

SI_NSE_100 <- round(SI_NSE / max(SI_NSE) * 100)
SI_Nearing_NSE_100 <- round(SI_Nearing_NSE / max(abs(SI_Nearing_NSE)) * 400)
SI_Nearing_Q_100 <- round(SI_Nearing_Q / max(abs(SI_Nearing_Q)) * 300)

SI_All <- cbind(round(cbind(SI_NSE, SI_Nearing_NSE, SI_Nearing_Q), digits = 6), 
                SI_NSE_100, SI_Nearing_NSE_100, SI_Nearing_Q_100)
