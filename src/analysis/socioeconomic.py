import pandas as pd 
import geopandas as gpd 

def weight_accessibility(
    raw_distances: pd.Series,
    polygons: gpd.GeoDataFrame,
    weight_numerical: float,
    weight_subjective: float,
) -> pd.Series:
    """
    Applies socioeconomic and subjective weighting to raw network distances.
    
    Args:
        raw_distances: mean distance to N nearest HEIs (from compute_accessibility)
        polygons: GeoDataFrame with weighting variables
        weight_numerical: importance of numerical variable, in this case "INCOME" (0-1)
        weight_subjective: importance of the subjective variable, in this case "SATISFACTION WITH LIFE IN GENERAL" (0-1)
    
    Returns:
        Weighted accessibility score (higher = more disadvantaged)
    """
    
    #Requirement 1. Normalize income to 0-1 scale

    
    
    return 0