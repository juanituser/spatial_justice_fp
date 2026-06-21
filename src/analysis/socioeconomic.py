import pandas as pd 
import geopandas as gpd 
import logging

logger = logging.getLogger(__name__)

def normalize_variables(polygons: gpd.GeoDataFrame, variables: list) -> dict:
    """
    Normalizes multiple variables to 0-1 scale.
    
    Args:
        polygons: GeoDataFrame with the variables
        variables: list of column names to normalize
    
    Returns:
        Dictionary with {variable_name: normalized_series}
    """
    normalized = {}
    
    logger.info(f"---- Normalizing variables ----")

    for variable in variables:
        var_min = polygons[variable].min()
        var_max = polygons[variable].max()
        var_normalized = (polygons[variable] - var_min) / (var_max - var_min)
        normalized[variable] = var_normalized
    
    return normalized

def weight_accessibility(
    polygons: gpd.GeoDataFrame,
    numeric_vars: list,
    subjective_vars: list

) -> pd.Series:
    """
    Applies socioeconomic and subjective weighting to raw network distances.
    
    Args:
        raw_distances: mean distance to N nearest HEIs (from compute_accessibility)
        polygons: GeoDataFrame with the variables to weight
        weight_numerical: importance of numerical variable, in this case "INCOME" (0-1)
        weight_subjective: importance of the subjective variable, in this case "SATISFACTION WITH LIFE IN GENERAL" (0-1)
    
    Returns:
        Weighted accessibility score (higher = more disadvantaged)
    """
    
    # Used the normalize variables
    all_vars = numeric_vars + subjective_vars
    normalized = normalize_variables(polygons, all_vars)

    # Invert weight if needed: lower values → higher penalty

    
    return 0