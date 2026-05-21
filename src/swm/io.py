import geopandas as gpd
import logging

logger = logging.getLogger(__name__)

def load_geodata(filename, folder="data/"):
    
    logger.info(f"---- loading {filename} ----")

    gdf = gpd.read_file(folder + filename)
    
    if gdf.crs != 3116:
        logger.info(f"---- reprojecting to EPSG: 3116 ----")
        gdf = gdf.to_crs(epsg=3116)
    
    return gdf
