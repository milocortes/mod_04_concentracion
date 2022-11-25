import geopandas as gpd 
import matplotlib.pyplot as plt
from shapely.geometry import box
from fiona.crs import from_epsg
import rasterio
import pycrs

# Use geopandas to open Mexico City shp
cdmx_col = gpd.read_file("../datos/09colonias.geojson")
cdmx_col_dissolve = cdmx_col.dissolve("ENT")
cdmx_bounds = cdmx_col_dissolve.bounds.to_numpy().flatten()
minx, miny, maxx, maxy = cdmx_bounds[0], cdmx_bounds[2], cdmx_bounds[1], cdmx_bounds[3]

bbox = box(minx, miny, maxx, maxy)

geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

out_tif_path = "/home/milo/Documents/egtp/clases/licenciatura/concentracion/otros/raster_geodata_crop"

coords = getFeatures(geo)
out_img, out_transform = mask(raster=data, shapes=coords, crop=True)
# Copy the metadata
out_meta = data.meta.copy()
# Parse EPSG code
epsg_code = int(data.crs.data['init'][5:])

 out_meta.update({"driver": "GTiff",
   "height": out_img.shape[1],
   "width": out_img.shape[2],
   "transform": out_transform,
   "crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()})

with rasterio.open(out_tif, "w", **out_meta) as dest:
    dest.write(out_img)
import glob

files = glob.glob("/media/milo/KINGSTON/*.tif")

for f in files:
    src = rasterio.open(f)
    print(src.crs)

geo = geo.to_crs(crs=data.crs.data)