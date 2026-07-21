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

def load_weighting_config(config_file: str, folder="data/") -> dict:
    """
    Loads the CSV with variable names, weights, and direction.

    Returns:
        Dictionary: {variable_name: {"weight": float, "direction": str}}
    """
    logger.info(f"---- loading {config_file} ----")

    config = pd.read_csv(folder + config_file)

    # Validate if required columns exist or not
    required_cols = {"variable", "weight"}

    if not required_cols.issubset(config.columns):
        raise ValueError(f"Config file must contain columns: {required_cols}")

    # Default de direction si la columna no existe o hay celdas vacías
    if "direction" not in config.columns:
        logger.warning("No 'direction' column found in config. Assuming 'higher_better' for all variables.")
        config["direction"] = "higher_better"
    else:
        missing_direction = config["direction"].isna()
        if missing_direction.any():
            missing_vars = config.loc[missing_direction, "variable"].tolist()
            logger.warning(f"Missing direction for {missing_vars}. Assuming 'higher_better'.")
            config["direction"] = config["direction"].fillna("higher_better")

    # Validate allowed values
    valid_directions = {"higher_better", "lower_better"}
    invalid = ~config["direction"].isin(valid_directions)
    if invalid.any():
        invalid_rows = config.loc[invalid, ["variable", "direction"]]
        raise ValueError(f"Invalid direction values (must be 'higher_better' or 'lower_better'):\n{invalid_rows}")

    # Validate that the sum of the weights is 1
    weight_sum = config["weight"].sum()
    if abs(weight_sum - 1.0) > 1e-6:
        raise ValueError(f"Weights must sum to 1.0, got {weight_sum:.4f}")

    all_vars = {
        row["variable"]: {"weight": row["weight"], "direction": row["direction"]}
        for _, row in config.iterrows()
    }

    logger.info(f"Loaded {len(all_vars)} weighting variables from {config_file}")

    for name, var_config in all_vars.items():
        logger.info(f"  - {name}: weight={var_config['weight']}, direction={var_config['direction']}")

    return all_vars