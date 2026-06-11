import pandana
import geopandas as gpd


def register_pois(
    network:      pandana.Network,
    pois:         gpd.GeoDataFrame,
    max_distance: float,
    max_items:    int,
) -> None:
    """
    Registers POI locations on the pandana network.
    
    max_distance and max_items define the search area pandana prepares internally.
    
    Args:
        network:      pandana Network object
        pois:         GeoDataFrame of points of interest in WGS84
        max_distance: maximum search radius in meters
        max_items:    maximum number of POIs to return per node
    """
    network.set_pois(
        category="poi",
        maxdist=max_distance,
        maxitems=max_items,
        x_col=pois.geometry.x,
        y_col=pois.geometry.y,
    )
    print(f"POIs registered on network")