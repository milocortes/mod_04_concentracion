# Clase 5 Ecolog�a del movimiento: enfoques y an�lisis del movimiento animal.
# Objetivo: Estimar las �reas mediante los m�todos de Poligono Minimo Convexo y Kernel Density Estimator

# En caso de que no los tengan instalar los paquetes que vamos a utilizar en este ejercicio.
#install.packages("adehabitatHR")
#install.packages("move")
#install.packages("amt")


# 1. Primero vamos a trabajar en con el paquete adehabitatHR, para esto cargamos la libreria. 
### El sitio CRAN de esta libreria es la siguiente:
### https://cran.r-project.org/src/contrib/Archive/adehabitat/
library(adehabitatHR)
library(raster)
# 1.1 Abrimos el archivo con los datos de los 4 elefantes y vemos si R lo puede leer. 
kde_agua <-read.csv("kde_equipo_agua.csv",header=T)
kde_agua
head(kde_agua)

# 1.2  Primero voy a covertir los datos en "SpatialPolygonsDataFrame" que es el formato que utiliza adehabitatHR 
# para trabajar los datos y poder calcular las �reas de actividad
a <- cbind(kde_agua$lat, kde_agua$lon)
a

# 1.3  Ahora separo la columna con los nombre y creo un nuevo objeto pero como dataframe 
kde_agua$Id <- 1
b<- cbind(as.data.frame(kde_agua$Id))
b

# 1.4 Ahora creo un objeto "SpatialPointsDataFrame" utilizando las coordenadas y los nombres
kde_points<-SpatialPointsDataFrame(a,b)
kde_points



# 2. Ahora vamos a calcular el Kernel Density Estimator para con adehabitat para los 4 elefantes. Para esto utilizamos
# el comando kernelUD. Una parte importante de esto es definir el parametro de suavizado (smoothing parameter - h). El 
# parametro de suavizado controla el ancho de la funci�n kernel sobre cada localizaci�n. Ha existido mucho trabajo
# para definir la manera correcta del param�tro de suavizado para la estimaci�n de las �reas de actividad. Sin embargo,  
# las dos opciones comunes para hacer esto son "ancho de banda de referencia" (reference bandwidth), valiadaci�n cruzada de 
# minimos cuadrados Least Square Cross Validation (LSCV). En ejemplo siguiente lo hacemos por el "ancho de banda de referencia" 
# (reference bandwidth)
kde_fit <- kernelUD(kde_points[,1], h ="href", grid = 1000)
kde_fit
# Con el comando image vemos los kerneles Ahora vemos los kerneles con el comando image
image(kde_fit)

kde <- raster(as(kde_fit[[1]], "SpatialPixelsDataFrame"))

# sets projection to British National Grid

projection(kde) <- CRS("+init=EPSG:4326")

library(tmap)

# maps the raster in tmap, "ud" is the density variable
tm_shape(kde) + tm_raster("ud")

library(tmaptools) # provides a set of tools for processing spatial data

# creates a bounding box based on the extents of the Output.Areas polygon
bounding_box <- bb(kde_points)

# maps the raster within the bounding box
tm_shape(kde, bbox = bounding_box) + tm_raster("ud")


# compute homeranges for 75%, 50%, 25% of points, objects are returned as spatial polygon data frames
range75 <- getverticeshr(kde_fit, percent = 75)
range50 <- getverticeshr(kde_fit, percent = 50)
range25 <- getverticeshr(kde_fit, percent = 25)

# the code below creates a map of several layers using tmap
tm_shape(kde_points) + tm_dots(col = "blue") +
tm_shape(range75) + tm_borders(alpha=.7, col = "#fb6a4a", lwd = 2) + tm_fill(alpha=.1, col = "#fb6a4a") +
tm_shape(range50) + tm_borders(alpha=.7, col = "#de2d26", lwd = 2) + tm_fill(alpha=.1, col = "#de2d26") +
tm_shape(range25) + tm_borders(alpha=.7, col = "#a50f15", lwd = 2) + tm_fill(alpha=.1, col = "#a50f15") +
tm_layout(frame = FALSE)