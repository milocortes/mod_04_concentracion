from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import LineString, MultiPolygon, MultiPoint, Point
import pandas as pd

df = pd.read_excel("BASE LIMPIA 2.xlsx")

points =df[["LON","LAT"]].to_numpy().tolist()
vor = Voronoi(points)

import matplotlib.pyplot as plt
fig = voronoi_plot_2d(vor)
plt.show()


polygons = {}
for id, region_index in enumerate(vor.point_region):
    points = []
    for vertex_index in vor.regions[region_index]:
        if vertex_index != -1:  # the library uses this for infinity
            points.append(list(vor.vertices[vertex_index]))
    points.append(points[0])
    polygons[id]=points

import geopandas as gpd
from shapely.geometry import Polygon

geometria_voronoi = gpd.GeoSeries([Polygon(v) for k,v in polygons.items()])

gpd_estaciones_voronoi = gpd.GeoDataFrame(
    df.copy(), geometry=geometria_voronoi)

gdf_estaciones_puntos = gpd.GeoDataFrame(
    df.copy(), geometry=gpd.points_from_xy(df.LON, df.LAT))

gdf_estaciones_puntos["une"] = 1
gdf_estaciones_min_max = gdf_estaciones_puntos.dissolve("une")

minx, miny, maxx, maxy = gdf_estaciones_min_max.bounds.values.flatten()


fig, ax = plt.subplots(figsize=(15, 15))
gpd_estaciones_voronoi.boundary.plot(ax=ax, alpha=0.7, color="pink")
gdf_estaciones_puntos.plot(ax=ax)
plt.show()

gpd_estaciones_voronoi.to_file("voronoi.shp")
