## Para la descarga de los raster de precipitación vamos a usar la biblioteca geodata (https://cran.r-project.org/web/packages/geodata/geodata.pdf)
## Esta biblioteca descarga datos climáticos del CMIP6 para escenarios de clima futuros
## proyectados de worldclim (http://worldclim.com/formats1).
## Nos interesa los datos de precipitación. La unidad de medida de la precipitación
## es en milimetros, y refiere a la precipitación promedio mensual.
## La biblioteca permite la descarga de datos para distintos modelos de circulación general (GCM)
## así como para distintos Shared Socio-economic Pathway (SSP). También permite la 
## descarga para distintos periodos de tiempo  "2021-2040", "2041-2060", or "2061-2080"
## Nos interesa el dato con la mayor granularidad, por eso escogemos la resolución
## de 2.5 minutos

library(geodata)

ssp_list <- c("126", "245", "370", "585")

time_list <- c("2021-2040", "2041-2060", "2061-2080")

#gcm_list <- c("ACCESS-CM2", "AWI-CM-1-1-MR", "BCC-CSM2-MR", "CanESM5", 
#            "CanESM5-CanOE", "CMCC-ESM2", "CNRM-CM6-1", "CNRM-CM6-1-HR", "CNRMESM2-1", 
#            "EC-Earth3-Veg", "EC-Earth3-Veg-LR", "FIO-ESM-2-0", "GFDLESM4", "GISS-E2-1-G", 
#            "GISS-E2-1-H", "HadGEM3-GC31-LL", "INM-CM4-8", "INM-CM5-0", "IPSL-CM6A-LR", "MIROC-ES2L", 
#            "MIROC6", "MPIESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0", "UKESM1-0-LL")

gcm_list <- c("MIROC-ES2L", "MIROC6", "MPIESM1-2-HR", "MPI-ESM1-2-LR", "MRI-ESM2-0", "UKESM1-0-LL")


var_geo <- "prec"

resolution <- 2.5

download_path <- file.path("/home/milo/Documents/egtp/clases/licenciatura/concentracion/otros/geodata", "tiffs")

data_raster <- cmip6_world("CNRM-CM6-1", "585", "2061-2080", var=var_geo, res=resolution, path = download_path)

for(gcm in gcm_list){
    print("###############################")
    print("###############################")
    print(paste("          ", gcm,"       "))
    print("###############################")
    print("###############################")

    tryCatch(
        {
            for(ssp in ssp_list){
                for(time in time_list){
                    data_raster <- cmip6_world(gcm, ssp, time, var = var_geo, res = resolution, path = download_path)
                }
            }
        },
        error = function(e){
                print("###############################")
                print(paste(" ERROR --->", gcm,"       "))
                print("###############################")
        }
    )
}