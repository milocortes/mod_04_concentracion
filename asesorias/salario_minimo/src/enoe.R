#clear workspace
rm(list = ls(all = TRUE)) 

################# Cargamos las biblioecas necesarias ####################3
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



#### 21 ABRIL 2022

###############################################
### Definimos una ruta temporal para guardar los microdatos
temporal <- tempfile()
download.file("https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/enoe_n_2021_trim4_csv.zip",temporal)
files = unzip(temporal, list=TRUE)$Name
unzip(temporal, files=files[grepl("csv",files)])
sdemt <- read.csv("ENOEN_SDEMT421.csv")


# Se selecciona la población de referencia que es: población ocupada mayor de 15 años con entrevista completa y condición de residencia válida.
sdemt <- subset(sdemt, sdemt$clase2 == 1 & sdemt$eda>=15 & sdemt$eda<=98 & sdemt$r_def==0 & (sdemt$c_res==1 | sdemt$c_res==3))



domestico_df <- subset(sdemt, domestico == 8 | domestico == 3)

## Horas promedio trabajadas
wtd.mean(domestico_df$hrsocup, domestico_df$fac_tri)
## Ingreso promedio mensual
wtd.mean(domestico_df$ingocup, domestico_df$fac_tri)
## Ingreso promedio
wtd.mean(domestico_df$ing_x_hrs, domestico_df$fac_tri)
#
cruza_uno <- wtd.table(domestico_df$domestico, domestico_df$imssissste, domestico_df$fac_tri)

### Data frame para hacer el box plot

df_long_2022 <- data.frame(horas = domestico_df$hrsocup, ing_x_hrs = domestico_df$ing_x_hrs, etiqueta = rep("ENOE TRIM 4 2022", nrow(domestico_df)))
df_long_2021 <- data.frame(horas = domestico_df_2021$hrsocup, ing_x_hrs = domestico_df_2021$ing_x_hrs, etiqueta = rep("ENOE TRIM 4 2021", nrow(domestico_df_2021)))

df_long <- rbind.data.frame(df_long_2021, df_long_2022)

# Plot the chart.
boxplot(horas ~ etiqueta, data = df_long, xlab = "Trimeste ENOE",
   ylab = "Horas", main = "Comparación horas")


#### 
### ANÁLISIS DE HORAS ENTRE GRUPOS
#####

#clear workspace
rm(list = ls(all = TRUE)) 

################# Cargamos las biblioecas necesarias ####################3
library(questionr)
library(survey)
library(ggplot2)

###############################################
### Definimos una ruta temporal para guardar los microdatos
temporal <- tempfile()
download.file("https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/enoe_n_2021_trim4_csv.zip",temporal)
files = unzip(temporal, list=TRUE)$Name
unzip(temporal, files=files[grepl("csv",files)])
sdemt <- read.csv("ENOEN_SDEMT421.csv")


# Se selecciona la población de referencia que es: población ocupada mayor de 15 años con entrevista completa y condición de residencia válida.
sdemt <- subset(sdemt, sdemt$clase2 == 1 & sdemt$eda>=15 & sdemt$eda<=98 & sdemt$r_def==0 & (sdemt$c_res==1 | sdemt$c_res==3))


domestico_df <- subset(sdemt, domestico == 8 | domestico == 3)
domestico_df$etiqueta <- "domestico"

pea_total <- subset(sdemt, domestico == 1)
pea_total$etiqueta <- "pea"

df_groups <- rbind.data.frame(domestico_df[,c("hrsocup","etiqueta")], pea_total[,c("hrsocup","etiqueta")])

# Plot the chart.
boxplot(hrsocup ~ etiqueta, data = df_groups, xlab = "Grupo",
   ylab = "Horas", main = "Comparación horas")


# Without transparency (left)
ggplot(data=df_groups, aes(x=hrsocup, group=etiqueta, fill=etiqueta)) +
    geom_density(adjust=1.5) 

###
# Generamos primer grupo
solo_pea <- subset(sdemt, domestico == 1)
solo_pea$etiqueta <- "Solo PEA"

pea_quehaceres_domesticos <- subset(sdemt, domestico == 3)
pea_quehaceres_domesticos$etiqueta <- "PEA y quehaceres domésticos"

df_groups <- rbind.data.frame(solo_pea[,c("hrsocup","etiqueta")], pea_quehaceres_domesticos[,c("hrsocup","etiqueta")])


# Plot the chart.
boxplot(hrsocup ~ etiqueta, data = df_groups, xlab = "Grupo",
   ylab = "Horas", main = "Comparación horas")


# Without transparency (left)
ggplot(data=df_groups, aes(x=hrsocup, group=etiqueta, fill=etiqueta)) +
    geom_density(adjust=1.5) 


# Generamos primer grupo
apoyo_hogar <- subset(sdemt, domestico == 4)
apoyo_hogar$etiqueta <- "PEA y apoyos al hogar"

pea_quehaceres_domesticos <- subset(sdemt, domestico == 3)
pea_quehaceres_domesticos$etiqueta <- "PEA y quehaceres domésticos"

df_groups <- rbind.data.frame(apoyo_hogar[,c("hrsocup","etiqueta")], pea_quehaceres_domesticos[,c("hrsocup","etiqueta")])


# Plot the chart.
boxplot(hrsocup ~ etiqueta, data = df_groups, xlab = "Grupo",
   ylab = "Horas", main = "Comparación horas")


# Without transparency (left)
ggplot(data=df_groups, aes(x=hrsocup, group=etiqueta, fill=etiqueta)) +
    geom_density(adjust=1.5) 


####### AGREGANDO ESQUEMA DE MUESTREO

################# Cargamos las biblioecas necesarias ####################3
library(questionr)
library(survey)
library(ggplot2)

###############################################
### Definimos una ruta temporal para guardar los microdatos
temporal <- tempfile()
download.file("https://www.inegi.org.mx/contenidos/programas/enoe/15ymas/microdatos/enoe_n_2021_trim4_csv.zip",temporal)
files = unzip(temporal, list=TRUE)$Name
unzip(temporal, files=files[grepl("csv",files)])
sdemt <- read.csv("ENOEN_SDEMT421.csv")


# Se selecciona la población de referencia que es: población ocupada mayor de 15 años con entrevista completa y condición de residencia válida.
sdemt <- subset(sdemt, sdemt$clase2 == 1 & sdemt$eda>=15 & sdemt$eda<=98 & sdemt$r_def==0 & (sdemt$c_res==1 | sdemt$c_res==3))

## Definimos la variable etiqueta para identificar los grupos de acuerdo a ciertas condiciones

sdemt$etiqueta<-0

sdemt$etiqueta[sdemt$ domestico == 4] <- "PEA y apoyos al hogar"
sdemt$etiqueta[sdemt$ domestico == 3] <- "PEA y quehaceres domésticos"


sdemt <- subset(sdemt, etiqueta!="0")
sdemt$etiqueta <- as.factor(sdemt$etiqueta)

sdemt$mh_fil2 <- as.factor(sdemt$mh_fil2)

## Definimos esquema de muestreo
mydesign<-svydesign(id=~upm, strata=~est_d_tri, weight=~fac_tri, data=sdemt, nest=TRUE)
options(survey.lonely.psu="adjust")


svyboxplot(hrsocup~etiqueta,mydesign,all.outliers=TRUE)


svytable(~hrsocup+etiqueta,design=mydesign,round=TRUE)

svymean(~interaction(etiqueta, hrsocup), mydesign)

# Plot the chart.
boxplot(ingocup ~ etiqueta, data = sdemt, xlab = "Grupo",
   ylab = "Horas", main = "Comparación horas")


# Without transparency (left)
ggplot(data=df_groups, aes(x=hrsocup, group=etiqueta, fill=etiqueta)) +
    geom_density(adjust=1.5) 

