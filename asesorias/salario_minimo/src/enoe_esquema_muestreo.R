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

# Definimos el esquema de muestreo
sdemtdesign<-svydesign(id=~upm, strata=~est_d_tri, weight=~fac_tri, data=sdemt, nest=TRUE)
options(survey.lonely.psu="adjust")

#### Medias ponderadas por grupo
## Horas promedio trabajadas
svyby(~hrsocup, ~domestico, sdemtdesign, svymean, vartype=c("se","cv"))

## Ingreso promedio mensual
svyby(~ingocup, ~domestico, sdemtdesign, svymean, vartype=c("se","cv"))

## Ingreso promedio por hora
svyby(~ing_x_hrs, ~domestico, sdemtdesign, svymean, vartype=c("se","cv"))

#### Medias ponderadas por más subpoblaciones (sexo y doméstico)
## Horas promedio trabajadas
svyby(~hrsocup, ~sex + domestico, sdemtdesign, svymean, vartype=c("se","cv"))

## Ingreso promedio mensual
svyby(~ingocup, ~sex + domestico, sdemtdesign, svymean, vartype=c("se","cv"))

## Ingreso promedio por hora
svyby(~ing_x_hrs, ~sex + domestico, sdemtdesign, svymean, vartype=c("se","cv"))


# Multiple linear regression
summary(svyglm(hrsocup ~ factor(sex) + factor(domestico) + eda, design=sdemtdesign, na.action = na.omit))
summary(svyglm(ing_x_hrs ~ factor(sex) + eda, design=sdemtdesign, na.action = na.omit))


## Definimos la variable etiqueta para identificar los grupos de acuerdo a ciertas condiciones
sdemt$etiqueta<-"PEA. No apoyo al hogar"
sdemt$etiqueta[sdemt$ domestico == 4 | sdemt$ domestico == 3] <- "PEA. Algún apoyo al hogar"

## Horas promedio trabajadas
# Definimos el esquema de muestreo
sdemtdesign<-svydesign(id=~upm, strata=~est_d_tri, weight=~fac_tri, data=sdemt, nest=TRUE)
options(survey.lonely.psu="adjust")

svyby(~hrsocup, ~etiqueta, sdemtdesign, svymean, vartype=c("se","cv"))


### RECURSO
### https://stats.oarc.ucla.edu/r/seminars/survey-data-analysis-with-r/