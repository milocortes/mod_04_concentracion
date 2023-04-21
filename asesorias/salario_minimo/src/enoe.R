#clear workspace
rm(list = ls(all = TRUE)) 

################# Cargamos las biblioecas necesarias ####################3
library(foreign)
library(questionr)
library(survey)

setwd("/home/milo/Documents/egtp/clases/licenciatura/ccm-2023/mod_04_concentracion/asesorias/salario_minimo/datos/enoe_n_2022_trim3_csv")
###################Cargado de Bases#######################################

sdemt319 <- read.csv("ENOEN_SDEMT322.csv")
minimal_sdemt <- sdemt319[,c("hrsocup","ingocup","ing_x_hrs","fac_tri")]

minimal_sdemt <- read.csv("minimal_sdemt.csv")
write.csv(minimal_sdemt,"minimal_sdemt.csv", row.names = FALSE)
########################### seleccionamos poblacion 15 aÃ±os o mas ############3
sdemt319$eda <- as.numeric(as.character(sdemt319$eda) )
sdemt319 <- subset (sdemt319, eda >= 15 & eda <= 98) ###

########################## Incorporamos el esquema de muestreo #############

mydesign<-svydesign(id=~upm, strata=~est_d_tri, weight=~fac_tri, data=sdemt319, nest=TRUE)
options(survey.lonely.psu="adjust")

domestico_df <- subset(sdemt319, domestico == 8 | domestico == 3  )

## Horas promedio trabajadas
wtd.mean(domestico_df$hrsocup, domestico_df$fac_tri)
## Ingreso promedio mensual
wtd.mean(domestico_df$ingocup, domestico_df$fac_tri)
## Ingreso promedio
wtd.mean(domestico_df$ing_x_hrs, domestico_df$fac_tri)
#
cruza_uno <- wtd.table(domestico_df$domestico, domestico_df$imssissste, domestico_df$fac_tri)
