import pandas as pd
import geopandas as gpd
import logging

logger = logging.getLogger(__name__)

def load_geodata(filename, folder="data/", reproject_to=None):
    
    logger.info(f"---- loading {filename} ----")

    gdf = gpd.read_file(folder + filename)
    
    if reproject_to is not None and gdf.crs != f"EPSG:{reproject_to}":
        logger.info(f"---- reprojecting to EPSG:{reproject_to} ----")
        gdf = gdf.to_crs(epsg=reproject_to)

    if gdf.geometry.isnull().sum() != 0:
        logger.info(f"---- Deleting {gdf.geometry.isnull().sum()} rows with empty geometry ----")
        gdf = gdf[gdf.geometry.notnull()]
        gdf = gdf[~gdf.geometry.is_empty]
    
    if not gdf.geometry.is_valid.all():
        invalid_count = (~gdf.geometry.is_valid).sum()
        logger.warning(f"---- Found {invalid_count} invalid geometries, attempting to fix ----")
        gdf.geometry = gdf.geometry.buffer(0)

    return gdf

def load_weighting_config(config_file, folder="data/"):
    """
    Reads weighting config CSV and returns variables and their weights.
    
    Returns:
        (Dict with variables names and its weights)
    """

    logger.info(f"---- loading {config_file} ----")

    config = pd.read_csv(folder + config_file)

    variable_name = config["variable_name"].tolist()
    weights = config["weight"].tolist()

    socioeconomic_variables = dict(zip(variable_name, weights))

    return socioeconomic_variables