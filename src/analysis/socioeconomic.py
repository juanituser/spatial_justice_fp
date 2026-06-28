import pandas as pd 
import geopandas as gpd 
import logging

logger = logging.getLogger(__name__)

def normalize_variables(polygons: gpd.GeoDataFrame, socioeconomic_vars: dict) -> dict:
    """
    Normalizes multiple variables to 0-1 scale.
    
    Args:
        polygons: GeoDataFrame with the variables
        variables: Dictionary with the name of the socioeconomic variables to include in the analysis and its weights
    
    Returns:
        Dictionary with {variable_name: normalized_series}
    """
    normalized = {}
    
    logger.info(f"---- Normalizing variables ----")

    vars = socioeconomic_vars.keys()

    for variable in vars:
        var_min = polygons[variable].min()
        var_max = polygons[variable].max()
        var_normalized = (polygons[variable] - var_min) / (var_max - var_min)
        normalized[variable] = var_normalized
    
    return normalized

def weight_accessibility(
    polygons: gpd.GeoDataFrame,
    socioeconomic_vars: dict

) -> pd.Series:
    """
    Applies socioeconomic and subjective weighting to raw network distances.
    
    Args:
        raw_distances: mean distance to N nearest HEIs (from compute_accessibility)
        polygons: GeoDataFrame with the variables to weight
        socioeconomic_vars: Dictionary with the name of the socioeconomic variables to include in the analysis and its weights 
    
    Returns:
        Weighted accessibility score (higher = more disadvantaged)
    """
    
    # Used the normalize variables
    all_vars = numeric_vars + subjective_vars
    normalized = normalize_variables(polygons, all_vars)

    # Invert weight if needed: lower values → higher penalty

    
    return 0