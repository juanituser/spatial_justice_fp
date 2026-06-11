import geopandas as gpd
import logging

logger = logging.getLogger(__name__)

def load_geodata(filename, folder="data/", reproject_to=None):
    
    logger.info(f"---- loading {filename} ----")

    gdf = gpd.read_file(folder + filename)
    
    if gdf.crs != reproject_to:
        logger.info(f"---- reprojecting to EPSG:{reproject_to} ----")
        gdf = gdf.to_crs(epsg=reproject_to)

    if gdf.geometry.isnull().sum() != 0:
        logger.info(f"---- Deleting {gdf.geometry.isnull().sum()} rows with empty geometry ----")
        gdf = gdf[gdf.geometry.notnull()]
        gdf = gdf[~gdf.geometry.is_empty]
    
    return gdf
