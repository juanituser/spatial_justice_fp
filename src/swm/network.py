import logging
import geopandas as gpd

logger = logging.getLogger(__name__)

def get_bbox_wgs84(gdf: gpd.GeoDataFrame):
    """
    Converts the GeoDataFrame extent to WGS84 and returns
    the bounding box as (west, south, east, north).

    osmnx requires lat/lon coordinates — we convert here
    once and reuse the result for all OSM downloads.
    The GeoDataFrame itself stays in EPSG:3116.

    Args:
        gdf: GeoDataFrame in any projected CRS

    Returns:
        (west, south, east, north) in decimal degrees
    """

    gdf_wgs84 = gdf.to_crs(epsg=4326)

    west, south, east, north = gdf_wgs84.total_bounds
    print(f"Bounding box - W: {west:.4f} S: {south:.4f} E: {east:.4f} N: {north:.4f}")
    
    return west, south, east, north
