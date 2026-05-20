import logging

logger = logging.getLogger(__name__)

def get_bounding_box(gdf):
    
     
    logger.info(f"---- Bounding box for gdf with {len(gdf)} features ----")
    
    bbox = gdf.total_bounds
    
    logger.info(f"---- bbox result: {bbox} ----")

    return bbox

