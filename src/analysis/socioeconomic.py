import pandas as pd 
import geopandas as gpd 
import logging

logger = logging.getLogger(__name__)

def normalize_variables(polygons: gpd.GeoDataFrame, socioeconomic_vars: dict) -> dict:
    """
    Normalizes multiple variables to 0-1 scale, respecting each
    variable's direction (higher_better or lower_better).

    Args:
        polygons: GeoDataFrame with the variables
        socioeconomic_vars: {variable_name: {"weight": float, "direction": str}}

    Returns:
        Dictionary with {variable_name: normalized_series}, where higher
        values always mean "better" regardless of the original direction.
    """
    normalized = {}
    logger.info("---- Normalizing variables ----")

    print(socioeconomic_vars)

    for variable, config in socioeconomic_vars.items():
        var_min = polygons[variable].min()
        var_max = polygons[variable].max()

        var_normalized = (polygons[variable] - var_min) / (var_max - var_min)

        # Invert direction if lower is better
        if config["direction"] == "lower_better":
            var_normalized = 1 - var_normalized

        normalized[variable] = var_normalized
        logger.info(
            f"  - {variable}: min={var_min:.2f}, max={var_max:.2f}, "
            f"direction={config['direction']}"
        )

    return normalized


def weight_accessibility(
    accessibility: pd.DataFrame,
    polygons: gpd.GeoDataFrame,
    socioeconomic_vars: dict,
    distance_col: str = "mean_dist",
) -> pd.Series:
    """
    Applies socioeconomic weighting to raw accessibility distances, producing a spatial-justice index: districts that are both far from POIs and socioeconomically disadvantaged get an amplified effective distance.

    Args:
        accessibility: DataFrame from compute_accessibility
                       (dist_1...dist_N, mean_dist, opportunities),
                       indexed by district_id
        polygons: GeoDataFrame with socioeconomic variables,
                  indexed by district_id
        socioeconomic_vars: {variable_name: {"weight": float, "direction": str}}
        distance_col: which column of `accessibility` to use as the base distance

    Returns:
        pd.Series indexed by district_id. Higher = more disadvantaged
        (far from POIs AND socioeconomically vulnerable).
    """
    ## Normalized variables
    normalized = normalize_variables(polygons, socioeconomic_vars)

    penalty = sum(
    cfg["weight"] * (1 - normalized[var])
    for var, cfg in socioeconomic_vars.items()
)

    base_distance = accessibility[distance_col]

    # Amplify raw distance by socioeconomic penalty: a disadvantaged
    # district's *effective* distance grows, even if its raw distance is short.
    result = base_distance * (1 + penalty)

    logger.info(
        f"Weighted accessibility computed for {len(result)} districts "
        f"(base column: '{distance_col}')"
    )

    return result