import logging
import pandana
import pandas as pd
import geopandas as gpd


logger = logging.getLogger(__name__)

def compute_accessibility(
    network: pandana.Network,
    centroids: gpd.GeoDataFrame,
    max_distance: float,
    num_pois: int,
) -> pd.DataFrame:
    """
    Computes accessibility metrics for every district (every row in `centroids`).

    Returns a DataFrame indexed by the same index as `centroids`, with columns:
        dist_1 ... dist_N   — distance to the Nth nearest POI (meters)
        mean_dist            — average distance to the N nearest POIs
        opportunities         — count of POIs reachable within max_distance

    Args:
        network:      pandana Network with POIs already registered
        centroids:    GeoDataFrame of district centroids (index = district id)
        pois:         GeoDataFrame of points of interest (unused directly here,
                      kept for future use / consistency of the pipeline)
        max_distance: search radius in meters
        num_pois:     number of nearest POIs to compute distances for
    """

    # 1. Snap each district centroid to its closest network node
    centroids = centroids.copy()
    centroids["closest_node"] = network.get_node_ids(centroids.geometry.x, centroids.geometry.y)

    # 2. Precompute the network up to max_distance so queries below are fast.
    network.precompute(max_distance)

    # 3. Ask for each node, the distance to the N nearest POIs. This is indexed by node_id, not by district.
    distances_by_node = network.nearest_pois(
        distance=max_distance,
        category="poi",
        num_pois=num_pois,
        include_poi_ids=True,
    )

    # 4. Select only the rows corresponding to our district centroids' nodes.
    district_distances = distances_by_node.loc[centroids["closest_node"]]
    district_distances.index = centroids.index
    district_distances.index.name = centroids.index.name or "district_id"

    # 5. Keep only the first num_pois distance columns, renamed clearly.
    dist_cols = list(range(1, num_pois + 1))
    district_distances = district_distances[dist_cols]
    district_distances.columns = [f"dist_{i}" for i in range(1, num_pois + 1)]

    # 6. Mean distance to the N nearest POIs — one summary number per district.
    district_distances["mean_dist"] = district_distances.mean(axis=1)

    # 7. Opportunities: save how many of the N nearest POIs are actually within max_distance.
    opportunity_cols = [f"dist_{i}" for i in range(1, num_pois + 1)]
    district_distances["opportunities"] = (district_distances[opportunity_cols] < max_distance).sum(axis=1)

    logger.info(f"Accessibility computed for {len(district_distances)} districts")

    return district_distances