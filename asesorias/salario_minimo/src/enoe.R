#clear workspace
rm(list = ls(all = TRUE)) 

################# Cargamos las biblioecas necesarias ####################3
library(foreign)
library(questionr)
library(survey)

setwd("/home/milo/Documents/egtp/clases/licenciatura/ccm-2023/mod_04_concentracion/asesorias/salario_minimo/datos/enoe_n_2022_trim3_csv")
###################Cargado de Bases#######################################

sdemt319 <- read.csv("ENOEN_SDEMT322.csv")


