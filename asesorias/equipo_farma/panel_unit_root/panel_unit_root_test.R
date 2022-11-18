#### Limpiamos espacio de trabajo
rm(list = ls())

#### Cargamos las bibliotecas
library(plm)
library(stargazer)
library(ggplot2)

#### Haremos un ejemplo con series simuladas AR(1)

sequencia_date <-  seq(as.Date("2008/01/01/", format = "%Y/%m/%d"), as.Date("2020/01/01/", format = "%Y/%m/%d"),"months")
cve_entidades <- c(1:32)

# Definimos media y desviación del término de error para
mu <- 0
sigma <- 1
n <- length(sequencia_date)

df_entidades_simulados <- data.frame()

for(ent in cve_entidades){
  # Creamos el término de error para generar la serie AR(1)
  e <- rnorm(n,0,1)
  serie_ent <- abs(cumsum(e))

  df_ent <- data.frame(ent = rep(ent,n), date = sequencia_date, value = serie_ent)

  df_entidades_simulados <- rbind.data.frame(df_entidades_simulados,df_ent)
}

# Visualizamos los datos
ggplot(df_entidades_simulados, aes(x = date, y = value)) + 
  geom_line(aes(color = factor(ent))) 

# Definimos el formato de data.frame que necesita la biblioteca plm
df_entidades_simulados_p <- pdata.frame(df_entidades_simulados, index=c("ent", "date"))

# Realizamos la prueba para los 0,1 y 2 rezagos y con "trend", "drift" y "none"
# Guardamos los resultados en el data.frame resultados

resultados <- data.frame(lags = c(1:3))

for (tipo in c("trend", "drift", "none")) {
  resultados_tipo <-vector()
  for (lag in c(0,1,2)) {
    prueba <-cipstest(df_entidades_simulados_p$value, lags=lag, type = tipo, model ="dmg")
    resultados_tipo[lag+1]<-prueba$statistic[[1]]
  }    
  resultados_df<-as.data.frame(resultados_tipo)
  colnames(resultados_df)<-paste(tipo,sep = "_")
  resultados<-cbind.data.frame(resultados,resultados_df)
}

# Imprimimos los resultados de las pruebas de raíz unitaria
# Comparamos los valores de prueba con los que vienen en la primer tabla de 
# la página 11 del pdf que les compartí. Ahí vienen los valores críticos de 
# cada estadístico. Como pueden ver, en todos los casos, el estadístico calculado 
# es menor al estadístico de tablas, de manera que, como es de esperar dado que 
# todas las series son AR(1), no podemos rechazar la Ho: No estacionariedad.

resultados

######
### Haremos la misma prueba de raiz unitaria en panel con las series observadas de desapariciones
#####
#### Cargamos los datos
homicidios <- read.csv("/home/milo/Documents/egap/clases/licenciatura/concentracion/mod04/github/mod_04_concentracion/asesorias/equipo_farma/panel_unit_root/series_criminales_short.csv")

#### Filtramos por los registros 2008 >
homicidios<- subset(homicidios,Año >=2008)

#### Agregamos el campo date
homicidios$date<-rep(seq(as.Date('2008-1-1'),to=as.Date('2020-12-1'),by='1 month'),times = 32)
homicidios <- homicidios[,c("date","nom_ent","cve_ent","Desaparecidos_H","Desaparecidos_M")]
homicidios$Desaparecidos_T <- homicidios$Desaparecidos_H + homicidios$Desaparecidos_M
homicidios_p <- pdata.frame(homicidios, index=c("nom_ent", "date"))

#### Pesaran (2007)

## cipstest: Cross-sectionally Augmented IPS Test for Unit Roots in Panel Models
## description : Cross-sectionally augmented Im, Pesaran and Shin (IPS) test for unit roots in panel models.
## details : This cross-sectionally augmented version of the IPS unit root test (H0: the pseries has a unit root)
## is a so-called second-generation panel unit root test: 
##      it is in fact robust against cross-sectional dependence, provided that the default type="cmg" is calculated.
##      Else one can obtain the standard (model="mg") or cross-sectionally demeaned (model="dmg") versions of the IPS test.
## Realizamos el test de Pesaran(2007) con trend

test_var<-c("Desaparecidos_H","Desaparecidos_M","Desaparecidos_T")

resultados <-data.frame(c(0,0,0))

for (i in c(4,5,6)) {
  for (tipo in c("trend", "drift", "none")) {
    resultados_tipo <-vector()
    for (lag in c(0,1,2)) {
      prueba <-cipstest(homicidios_p[,i],lags=lag, type = tipo, model ="dmg")
      resultados_tipo[lag+1]<-prueba$statistic[[1]]
    }    
    resultados_df<-as.data.frame(resultados_tipo)
    colnames(resultados_df)<-paste(test_var[i-3],tipo,sep = "_")
    resultados<-cbind.data.frame(resultados,resultados_df)
  }
}

resultados <- round(resultados[,-1],2)

stargazer(resultados,summary = FALSE)
