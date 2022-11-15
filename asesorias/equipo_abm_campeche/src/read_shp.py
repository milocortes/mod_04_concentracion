import geopandas as gpd
import matplotlib.pyplot as plt

tiendas = gpd.read_file("../data/INEGI_DENUE_03112022/INEGI_DENUE_03112022.shp")

tiendas = tiendas.to_crs({'init': 'epsg:4326'})

from shapely.geometry import MultiPoint,shape
import fiona
import shapely
import numpy as np

mpt = MultiPoint([shape(point['geometry']) for point in fiona.open("../data/INEGI_DENUE_03112022/INEGI_DENUE_03112022.shp")])
convex_hull_shapely = shapely.wkt.loads(mpt.convex_hull.wkt)


convex_hull_gpd = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[convex_hull_shapely])

# límites del geodataframe
x_min, y_min, x_max, y_max = convex_hull_gpd.total_bounds

# tamaño de muestra de los hogares
n = 40000
# generamos los hogares de forma aleatoria dentro de los límites
x = np.random.uniform(x_min, x_max, n)
y = np.random.uniform(y_min, y_max, n)

# convertimos los puntos a GeoSeries
gdf_points = gpd.GeoSeries(gpd.points_from_xy(x, y))
gdf_points = gdf_points.set_crs('epsg:4326')
# nos quedamos con los puntos dentro del polígono mínimo convexo
gdf_points = gdf_points[gdf_points.within(convex_hull_gpd.unary_union)]

fig, ax = plt.subplots(figsize=(15, 15))
tiendas.plot(ax=ax, alpha=0.7, color="pink")
gdf_points.plot(ax=ax)
plt.show()


### Reproyección de las unidades
# Modificamos el sistema de referencia para poder hacer calculos
# con unidades de medida de metros 
# https://epsg.io/4488

gdf_points = gdf_points.to_crs("EPSG:4488")
tiendas = tiendas.to_crs("EPSG:4488")

# Definimos la distancia del buffer en metros 
buffer_dist = 2000
gdf_tiendas_buffer = tiendas["geometry"].buffer(buffer_dist)

sub_min_distance = [any(gdf_tiendas_buffer.contains(hogar)) for hogar in gdf_points]

gdf_points = gdf_points[sub_min_distance].reset_index(drop=True)

tiendas.to_file("../output/tiendas_campeche.geojson", driver='GeoJSON')
tiendas.to_file("../output/tiendas_campeche.shp")

gdf_points.to_file("../output/hogares_random.geojson", driver='GeoJSON')
gdf_points.to_file("../output/hogares_random.shp")
