library(tidyverse)
theme_set(theme_bw())
library(zoo)
library(gridExtra)
library(ggpubr)
library(cowplot)
library(ggthemes)
library(patchwork)
library(xts)
color_LK <- c("#c91f37", "#ff2121", "#f47983", # red
              "#ee7f00", "#fcf067", "#c6c932", # yellow
              "#69af22", "#007d3f", "#009966", # green
              "#006ab2", "#009de0", "#00305d", # blue
              "#6633cc", "#93107d", "#54368a") # lila
setwd("E:\\Kan_Lei\\Raven_Kreischa\\Raven_Kreischa_R\\plot")
## time
cali_Date <- as.Date(1095:2921, origin = "2001-01-01")
vali1_Date <- as.Date(index_start_raven1:index_end_raven1 - 2, origin = "2001-01-01")
vali2_Date <- as.Date(index_start_raven2:index_end_raven2 - 2, origin = "2001-01-01")
## table export list

table_list <- list(best_param_cali1, best_gof_cali1,
                   best_param_cali2, best_gof_cali2,
                   best_param_cali3, best_gof_cali3,
                   SI_all)
save(table_list, file = "table_list.RData")
## cali1 ####

setwd("E:\\Kan_Lei\\Raven_Kreischa\\model_files")
gof_Cali <- read.table("log_cali_gof.txt")
param_Cali <- read.table("log_cali_param.txt")

cali_Raven(param_Cali[order(gof_Cali$V1)[1],], Model_Name, n_Warmup, Q_Observ)
Q_Raven <- read.csv("cali_Hydrographs.csv")

plotcali1 <- ggplot() +
  geom_line(aes(cali_Date, Q_Observ), color = "blue") +
geom_line(aes(cali_Date, Q_Raven$KS_53719235..m3.s.[-(1:n_Warmup)]), color = "red") +
  scale_x_date(expand = c(0,0)) +
  xlab(expression(paste("Datum [-]"))) +
  ylab(expression(paste("Durchfluss [m"^3,"/s]")))
ggsave("plotcali1.png", plotcali1, "png", width = 9, height = 5.2, dpi = 600)


## sensi ####
df_NSE_Sensi <- as.data.frame(NSE_Sensi)
names(df_NSE_Sensi) <- Param_Name
NSE_Sensi_fixed <- NSE_Sensi
NSE_Sensi_fixed[which(NSE_Sensi_fixed < -5)] <- NA

df_Q_Sensi <- as.data.frame(Q_Sensi)
names(df_Q_Sensi) <- Param_Name
Q_Sensi_fixed <- Q_Sensi
Q_Sensi_fixed[which(Q_Sensi_fixed > 1)] <- NA


## Soil
table_NSE_Soil <- data.frame(Parameter = Param_Name[1:8], maxi_NSE = apply(NSE_Sensi_fixed[,1:8], 2, max), SI = apply(NSE_Sensi_fixed[,1:8], 2, sensi_index_NSE))
df_NSE_Soil <- data.frame(x = rep(1:n_dis), y = as.numeric(NSE_Sensi[,1:8]), param = rep(Param_Name[1:8], each = n_dis))
df_Q_Soil <- data.frame(x = rep(1:n_dis), y = as.numeric(Q_Sensi[,1:8]), param = rep(Param_Name[1:8], each = n_dis))

plot_NSE_soil <- ggplot(df_NSE_Soil) +
  geom_line(aes(x = x, y = y, colour = param), size = 1) +
  scale_color_discrete("Parameter", breaks = Param_Name[1:8])+
  ylab("NSE") +
  xlab("Boden Parameter Parameterbereichen") + 
  coord_cartesian(ylim = c(-3, 1)) + 
  scale_x_continuous(breaks = c(1,n_dis), labels = c("min", "max"), expand = c(0,0))
  # annotation_custom(tableGrob(table_NSE_Soil, theme = ttheme_minimal(base_size = 10)), xmin=9, xmax=12, ymin=-1, ymax=0)

plot_Q_soil <-
  ggplot(df_Q_Soil) +
  geom_line(aes(x = x, y = y, colour = param), size = 1) +
  scale_color_discrete("Parameter", breaks = Param_Name[1:8])+
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  xlab("Boden Parameter Parameterbereichen") + 
  coord_cartesian(ylim = c(0.3, 1)) + 
  scale_x_continuous(breaks = c(1,n_dis), labels = c("min", "max"), expand = c(0,0))

plot_soil <- plot_NSE_soil + plot_Q_soil +
  plot_layout(ncol = 2, guides = "collect") 

ggsave("plot_soil.png",plot_soil, "png", width = 11, height = 5)
## Veg
table_NSE_Veg <- data.frame(Parameter = Param_Name[9:15], maxi_NSE = apply(NSE_Sensi_fixed[,9:15], 2, max), SI = apply(NSE_Sensi_fixed[,9:15], 2, sensi_index_NSE))
df_NSE_Veg <- data.frame(x = rep(1:n_dis), y = as.numeric(NSE_Sensi[,9:15]), param = rep(Param_Name[9:15], each = n_dis))
df_Q_Veg <- data.frame(x = rep(1:n_dis), y = as.numeric(Q_Sensi[,9:15]), param = rep(Param_Name[9:15], each = n_dis))
plot_NSE_Veg <- ggplot(df_NSE_Veg) +
  geom_line(aes(x = x, y = y, colour = param), size = 1) +
  scale_color_discrete("Parameter", breaks = Param_Name[9:15])+
  ylab("NSE") +
  xlab("Pflanzen Parameter Parameterbereichen") + 
  coord_cartesian(ylim = c(0.65, 0.66)) + 
  scale_x_continuous(breaks = c(1,n_dis), labels = c("min", "max"), expand = c(0,0))
  # annotation_custom(tableGrob(table_NSE_Veg, theme = ttheme_minimal(base_size = 10)), xmin=9, xmax=12, ymin=.295, ymax=.31)

plot_Q_Veg <-
  ggplot(df_Q_Veg) +
  geom_line(aes(x = x, y = y, colour = param), size = 1) +
  scale_color_discrete("Parameter", breaks = Param_Name[9:15])+
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  xlab("Pflanzen Parameter Parameterbereichen") + 
  coord_cartesian(ylim = c(0.35, 0.375)) + 
  scale_x_continuous(breaks = c(1,n_dis), labels = c("min", "max"), expand = c(0,0))
plot_Veg <- plot_NSE_Veg + plot_Q_Veg +
  plot_layout(ncol = 2, guides = "collect") 

ggsave("plot_Veg.png",plot_Veg, "png", width = 11, height = 5)


## Land
table_NSE_Land <- data.frame(Parameter = Param_Name[16:20], maxi_NSE = apply(NSE_Sensi_fixed[,16:20], 2, max), SI = apply(NSE_Sensi_fixed[,16:20], 2, sensi_index_NSE))
df_NSE_Land <- data.frame(x = rep(1:n_dis), y = as.numeric(NSE_Sensi[,16:20]), param = rep(Param_Name[16:20], each = n_dis))
df_Q_Land <- data.frame(x = rep(1:n_dis), y = as.numeric(Q_Sensi[,16:20]), param = rep(Param_Name[16:20], each = n_dis))
plot_NSE_Land <-
  ggplot(df_NSE_Land) +
  geom_line(aes(x = x, y = y, colour = param), size = 1) +
  scale_color_discrete("Parameter", breaks = Param_Name[16:20])+
  ylab("NSE") +
  xlab("Landnutzung Parameter Parameterbereichen") + 
  coord_cartesian(ylim = c(0.4, 0.7)) + 
  scale_x_continuous(breaks = c(1,n_dis), labels = c("min", "max"), expand = c(0,0))
  # annotation_custom(tableGrob(table_NSE_Land, theme = ttheme_minimal(base_size = 10)), xmin=9, xmax=12, ymin=0.5, ymax=0.6)

plot_Q_Land <-
  ggplot(df_Q_Land) +
  geom_line(aes(x = x, y = y, colour = param), size = 1) +
  scale_color_discrete("Parameter", breaks = Param_Name[16:20])+
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  xlab("Landnutzung Parameter Parameterbereichen") + 
  coord_cartesian(ylim = c(0.359, 0.362)) + 
  scale_x_continuous(breaks = c(1,n_dis), labels = c("min", "max"), expand = c(0,0))

plot_Land <- plot_NSE_Land + plot_Q_Land +
  plot_layout(ncol = 2, guides = "collect") 

ggsave("plot_Land.png",plot_Land, "png", width = 11, height = 5)


plotcali1 <-
  ggplot() +
  geom_line(aes(cali_Date, Q_Observ, colour = "Beobachtung")) +
  geom_line(aes(cali_Date, Q_Raven_C1$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "C1\nNSE = 0,652"), size = 0.3) +
  scale_x_date(expand = c(0,0)) +
  xlab(expression(paste("Datum [-]"))) +
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  scale_color_manual("", values = c("blue", "red", "green", "yellow")) +
  theme(legend.position = "top")
ggsave("plotcali1.png", plotcali1, "png", width = 9, height = 4.5, dpi = 600)

## cali2&3 ####
plotcali3 <-
  ggplot() +
  geom_line(aes(cali_Date, Q_Observ, colour = "Beobachtung")) +
  geom_line(aes(cali_Date, Q_Raven_C1$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "C1\nNSE = 0,652"), size = 0.2) +
  geom_line(aes(cali_Date, Q_Raven_C2$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "C2\nNSE = 0,784"), size = 0.4) +
  geom_line(aes(cali_Date, Q_Raven_C3$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "C3\nNSE = 0,762"), size = 0.2) +
  scale_x_date(expand = c(0,0)) +
  xlab(expression(paste("Datum [-]"))) +
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  scale_color_manual("", values = c("blue", "red", "green", "yellow")) +
  theme(legend.position = "top")
ggsave("plotcali3.png", plotcali3, "png", width = 9, height = 4.5, dpi = 600)

plotcali2004 <-
  ggplot() +
  geom_line(aes(cali_Date[1:366], Q_Observ[1:366], colour = "Beobachtung")) +
  geom_line(aes(cali_Date[1:366], Q_Raven_C1$KS_53719235..m3.s.[n_Warmup:(n_Warmup+365)], colour = "C1\nNSE = 0,652"), size = 0.2) +
  geom_line(aes(cali_Date[1:366], Q_Raven_C2$KS_53719235..m3.s.[n_Warmup:(n_Warmup+365)], colour = "C2\nNSE = 0,784"), size = 0.4) +
  geom_line(aes(cali_Date[1:366], Q_Raven_C3$KS_53719235..m3.s.[n_Warmup:(n_Warmup+365)], colour = "C3\nNSE = 0,762"), size = 0.2) +
  scale_x_date(expand = c(0,0)) +
  xlab(expression(paste("Jahr 2004 [-]"))) +
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  scale_color_manual("", values = c("blue", "red", "green", "yellow")) +
  theme(legend.position = "top")
ggsave("plotcali2004.png", plotcali2004, "png", width = 9, height = 4.5, dpi = 600)



# geom_line(aes(cali_Date, Q_Observ, colour = "Beobachtung"), color = "blue") +
#   geom_line(aes(cali_Date, Q_Raven$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "1. Kalibrierung"), color = "red", alpha = 0.5) +
#   geom_line(aes(cali_Date, Q_Raven2$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "2.1. Kalibrierung"), color = "yellow", alpha = 0.5) +
#   geom_line(aes(cali_Date, Q_Raven3$KS_53719235..m3.s.[-(1:n_Warmup)], colour = "2.2. Kalibrierung"), color = "green") +
#   



## vali1 ####
plotvali1 <-
  ggplot() +
  geom_line(aes(vali1_Date, Q_Kreischa_V1, colour = "Beobachtung")) +
  geom_line(aes(vali1_Date, Q_Raven_V11, colour = "C1-NSE = 0,652\nV11-NSE = 0,658"), size = 0.2) +
  geom_line(aes(vali1_Date, Q_Raven_V21, colour = "C2-NSE = 0,784\nV21-NSE = 0,742"), size = 0.4) +
  geom_line(aes(vali1_Date, Q_Raven_V31, colour = "C3-NSE = 0,762\nV31-NSE = 0,742"), size = 0.2) +
  scale_x_date(expand = c(0,0)) +
  xlab(expression(paste("Datum [-]"))) +
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  scale_color_manual("", values = c("blue", "red", "green", "yellow")) +
  theme(legend.position = "top")
ggsave("plotvali1.png", plotvali1, "png", width = 9, height = 4.5, dpi = 600)


## vali2 ####
plotvali2 <-
  ggplot() +
  geom_line(aes(vali2_Date, Q_Kreischa_V2, colour = "Beobachtung")) +
  geom_line(aes(vali2_Date, Q_Raven_V12, colour = "C1-NSE = 0,652\nV12-NSE = 0,678"), size = 0.2) +
  geom_line(aes(vali2_Date, Q_Raven_V22, colour = "C2-NSE = 0,784\nV22-NSE = 0,730"), size = 0.4) +
  geom_line(aes(vali2_Date, Q_Raven_V32, colour = "C3-NSE = 0,762\nV32-NSE = 0,729"), size = 0.2) +
  scale_x_date(expand = c(0,0)) +
  xlab(expression(paste("Datum [-]"))) +
  ylab(expression(paste("Durchfluss [m"^3,"/s]"))) +
  scale_color_manual("", values = c("blue", "red", "green", "yellow")) +
  theme(legend.position = "top")
ggsave("plotvali2.png", plotvali2, "png", width = 9, height = 4.5, dpi = 600)



## Dopellsummenanalyse ####
reihe_x <- meteo_991$RAINFALL[index_start_meteo_c:index_end_meteo_c]
reihe_y1 <- meteo_991$RAINFALL[index_start_meteo_v1:index_end_meteo_v1]
reihe_y2 <- meteo_991$RAINFALL[index_start_meteo_v2:index_end_meteo_v2]
cum_sum_x <- cumsum(reihe_x)
cum_sum_y1 <- cumsum(reihe_y1)
cum_sum_y2 <- cumsum(reihe_y2)
b_av1 <- sum(reihe_y1) / sum(reihe_x)
b_av2 <- sum(reihe_y2) / sum(reihe_x)
plotdplregen <-
ggplot() +
  geom_line(aes(x = c(0, sum(reihe_x)), y = c(0, sum(reihe_y1))), color = 'darkred', linetype = 'longdash')+
  geom_line(aes(x = cum_sum_x, y = cum_sum_y1, color = '2009 - 2013'))+
  geom_line(aes(x = c(0, sum(reihe_y1)), y = c(0, b_av2 * sum(reihe_y1))), color = 'red', linetype = 'longdash')+
  geom_line(aes(x = cum_sum_x, y = cum_sum_y2, color = '2015 - 2019'))+
  scale_color_manual("", values = c("darkblue", "cyan")) +
  theme(legend.position = 'none', aspect.ratio = 1)+
  scale_x_continuous(expand = c(0,0), limits = c(0, sum(reihe_y1))) +
  scale_y_continuous(expand = c(0,0), limits = c(0, sum(reihe_y1))) +
  xlab(expression(paste("Summenlinie von Regen 2004 - 2008 [mm]"))) +
  ylab(expression(paste("Summenlinie von Regen [mm]"))) +
  geom_text(aes(1000, 3500, label = paste0("y = ", round(b_av1,4), " * x")), nudge_y = 100, color = 'darkred') +
geom_text(aes(1000, 3500, label = paste0("y = ", round(b_av2,4), " * x")), nudge_y = -100, color = 'red')

reihe_x_snow <- meteo_991$SNOWFALL[index_start_meteo_c:index_end_meteo_c]
reihe_y1_snow <- meteo_991$SNOWFALL[index_start_meteo_v1:index_end_meteo_v1]
reihe_y2_snow <- meteo_991$SNOWFALL[index_start_meteo_v2:index_end_meteo_v2]
cum_sum_x_snow <- cumsum(reihe_x_snow)
cum_sum_y1_snow <- cumsum(reihe_y1_snow)
cum_sum_y2_snow <- cumsum(reihe_y2_snow)
b_av1_snow <- sum(reihe_y1_snow) / sum(reihe_x_snow)
b_av2_snow <- sum(reihe_y2_snow) / sum(reihe_x_snow)
plotdplschnee <-
ggplot() +
  geom_line(aes(x = c(0, sum(reihe_x_snow)), y = c(0, sum(reihe_y1_snow))), color = 'darkred', linetype = 'longdash')+
  geom_line(aes(x = cum_sum_x_snow, y = cum_sum_y1_snow, color = '2009 - 2013'))+
  geom_line(aes(x = c(0, sum(reihe_x_snow)), y = c(0, sum(reihe_y2_snow))), color = 'red', linetype = 'longdash')+
  geom_line(aes(x = cum_sum_x_snow, y = cum_sum_y2_snow, color = '2015 - 2019'))+
  scale_color_manual("", values = c("darkblue", "cyan")) +
  theme(legend.position = 'none', aspect.ratio = 1)+
  scale_x_continuous(expand = c(0,0), limits = c(0, sum(reihe_x_snow))) +
  scale_y_continuous(expand = c(0,0), limits = c(0, sum(reihe_x_snow))) +
  # coord_fixed()+
  xlab(expression(paste("Summenlinie von Schnee 2004 - 2008 [mm]"))) +
  ylab(expression(paste("Summenlinie von Schnee [mm]")))+
  geom_text(aes(150, 700, label = paste0("y = ", round(b_av1_snow,4), " * x")), nudge_y = 50, color = 'darkred') +
  geom_text(aes(150, 700, label = paste0("y = ", round(b_av2_snow,4), " * x")), nudge_y = -50, color = 'red')

## temperatur
reihe_c_t <- meteo_991$TEMP_AVE[index_start_meteo_c:index_end_meteo_c]
reihe_v1_t <- meteo_991$TEMP_AVE[index_start_meteo_v1:index_end_meteo_v1]
reihe_v2_t <- meteo_991$TEMP_AVE[index_start_meteo_v2:index_end_meteo_v2]
sort_reihe_c_t <- sort(reihe_c_t)
sort_reihe_v1_t <- sort(reihe_v1_t)
sort_reihe_v2_t <- sort(reihe_v2_t)
plotdauerlT <- 
ggplot() +
  geom_line(aes(x = 1:1826, y = sort_reihe_c_t, color = '2004 - 2008'))+
  geom_line(aes(x = 1:1826, y = sort_reihe_v1_t, color = '2009 - 2013'))+
  geom_line(aes(x = 1:1826, y = sort_reihe_v2_t, color = '2015 - 2019'))+
  scale_color_manual("", values = c('darkred', "darkblue", "cyan")) +
  theme(legend.position = 'none', aspect.ratio = 1)+
  scale_x_continuous(expand = c(0,0)) +
  xlab(expression(paste("Temperaturdauerlinie in 5 Jahren [-]"))) +
  ylab(expression(paste("Temperatur [°C]")))




t_monate_c <- matrix(reihe_c_t[1:1800], 30, 60) |> colMeans()
t_monate_v1 <- matrix(reihe_v1_t[1:1800], 30, 60) |> colMeans()
t_monate_v2 <- matrix(reihe_v2_t[1:1800], 30, 60) |> colMeans()
t_quart <- xts(meteo_991$TEMP_AVE, as.Date(Q_Kreischa$Datum[1:7305], tryFormats = "%d.%m.%Y")) |> 
  apply.quarterly(mean)
plotglinieT <-
ggplot() +
  geom_line(aes(x = 1:60, y = t_monate_c, color = '2004 - 2008'))+
  geom_line(aes(x = 1:60, y = t_monate_v1, color = '2009 - 2013'))+
  geom_line(aes(x = 1:60, y = t_monate_v2, color = '2015 - 2019'))+
  scale_color_manual("", values = c('darkred', "darkblue", "cyan")) +
  scale_x_continuous(expand = c(0,0)) +
  # scale_y_continuous(expand = c(0,0)) +
  # coord_fixed()+
  xlab(expression(paste("Monatliche Temperatur in 5 Jahren [-]"))) +
  ylab(expression(paste("Temperatur [°C]")))
  # geom_text(aes(150, 700, label = paste0("y = ", round(b_av1_snow,4), " * x")), nudge_y = 50, color = 'darkred') +
  # geom_text(aes(150, 700, label = paste0("y = ", round(b_av2_snow,4), " * x")), nudge_y = -50, color = 'red')
plotgangallT <- 
ggplot() +
  geom_rect(aes(xmin = index(t_year)[4], xmax = index(t_year)[9], ymin = -4, ymax = 19), fill = "yellow", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[6], y = 7.5, label = "Kalibrierung"), size = 20, angle = 90, color = "white") +
  geom_rect(aes(xmin = index(t_year)[9], xmax = index(t_year)[14], ymin = -4, ymax = 19), fill = "blue", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[11], y = 7.5, label = "Validierung 1"), size = 18, angle = 90, color = "white") +
  geom_rect(aes(xmin = index(t_year)[15], xmax = index(t_year)[20], ymin = -4, ymax = 19), fill = "cyan", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[17], y = 7.5, label = "Validierung 2"), size = 18, angle = 90, color = "white") +
  geom_line(aes(x = index(t_quart), y = t_quart), color = 'darkred') +
  geom_line(aes(x = index(t_year), y = t_year), color = 'red') +
  scale_x_date(expand = c(0,0)) +
  scale_y_continuous(expand = c(0,0)) +
  xlab(expression(paste("Jahr [-]"))) +
  ylab(expression(paste("Temperatur [°C]")))



layout_design = "ABC
ABC
DDD
"
plothomo <-
  (plotdplregen + plotdplschnee + plotdauerlT  + plot_layout(nrow = 1, ncol = 3))+
    plotglinieT +
  plot_layout(nrow = 3, ncol = 3, byrow = T,
              design = layout_design, guides = "collect")
ggsave("plothomo.png", plothomo, "png", width = 13, height = 6.3, dpi = 800)







Q_Kreischa_xts <- xts(Q_Kreischa$Durchfluss[1:7305], as.Date(Q_Kreischa$Datum[1:7305], tryFormats = "%d.%m.%Y"))
q_week <- apply.weekly(Q_Kreischa_xts, mean)
plotq3zeitraum <- ggplot() +
  geom_rect(aes(xmin = index(t_year)[1], xmax = index(t_year)[4], ymin = 0, ymax = 7), fill = "red", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[2], y = 3.5, label = "Warm-up"), size = 20, angle = 90, color = "white") +
  geom_rect(aes(xmin = index(t_year)[4], xmax = index(t_year)[9], ymin = 0, ymax = 7), fill = "purple", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[6], y = 3.5, label = "Kalibrierung"), size = 20, angle = 90, color = "white") +
  geom_rect(aes(xmin = index(t_year)[9], xmax = index(t_year)[14], ymin = 0, ymax = 7), fill = "blue", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[11], y = 3.5, label = "Validierung 1"), size = 18, angle = 90, color = "white") +
  geom_rect(aes(xmin = index(t_year)[15], xmax = index(t_year)[20], ymin = 0, ymax = 7), fill = "cyan", alpha = 0.3) +
  geom_text(aes(x = index(t_year)[17], y = 3.5, label = "Validierung 2"), size = 18, angle = 90, color = "white") +
  geom_line(aes(x = index(q_week), y = q_week), color = 'darkblue') +
  scale_x_date(expand = c(0,0)) +
  scale_y_continuous(expand = c(0,0)) +
  xlab(expression(paste("Jahr [-]"))) +
  ylab(expression(paste("Wöchentliches Durchfluss [m"^3,"/s]")))
ggsave("plotq3zeitraum.png", plotq3zeitraum, "png", width = 9.5, height = 4.7, dpi = 600)
