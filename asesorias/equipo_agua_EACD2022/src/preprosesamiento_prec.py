import geopandas
import rasterio
import matplotlib.pyplot as plt
from rasterstats import zonal_stats

# Use rasterio to open the raster data
src = rasterio.open('../wc2.1_2.5m/cdmx_wc2.1_2.5m_prec_CNRM-CM6-1_ssp585_2021-2040.tif')


# Use geopandas to open Mexico City shp
cdmx = geopandas.read_file("../datos/09mun.geojson")
#cdmx = cdmx.to_crs(4326)
cdmx = cdmx.to_crs({'init': 'epsg:4326'})

from rasterio.plot import show

fig, ax = plt.subplots()

# transform rasterio plot to real world coords
extent=[src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
ax = rasterio.plot.show(src, extent=extent, ax=ax, cmap='pink')
im = ax.get_images()[0]
fig.colorbar(im, ax=ax)

cdmx.boundary.plot(ax=ax)
plt.show()

# Zonal stats

zonal_stats(
        vectors=cdmx["geometry"],
        raster='../wc2.1_2.5m/cdmx_wc2.1_2.5m_prec_CNRM-CM6-1_ssp585_2021-2040.tif',
        stats='mean'
    )
