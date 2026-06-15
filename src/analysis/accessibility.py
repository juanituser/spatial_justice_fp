import pandana
import pandas as pd

def compute_accessibility(
    network:      pandana.Network,
    max_distance: float,
    num_pois:     int,
) -> pd.DataFrame:
    """
    Computes two accessibility metrics for every node in the network:

    1. dist_1...dist_N: distance in meters to the Nth nearest POI.
       Nodes with no POI within max_distance receive max_distance
       as the value. Lower is better.

    2. opportunities: count of POIs reachable within max_distance.
       Derived from the distance columns — any dist_N < max_distance
       counts as one reachable opportunity. Higher is better.

    Args:
        network:      pandana Network with POIs already registered
        max_distance: search radius in meters
        num_pois:     number of nearest POIs to compute distances for

    Returns:
        DataFrame indexed by node_id with columns:
            dist_1 ... dist_N  — distance to Nth nearest POI
            opportunities      — count of POIs within max_distance
    """
    print(f"Precomputing network reachability up to {max_distance}m...")
    network.precompute(max_distance)

    distances = network.nearest_pois(
        distance=max_distance,
        category="poi",
        num_pois=num_pois,
        max_distance=max_distance,
    )
    print(distances)
    distances.columns = [f"dist_{i}" for i in range(1, num_pois + 1)]

    distances["opportunities"] = (distances < max_distance).sum(axis=1)

    print(f"Accessibility computed for {len(distances)} network nodes")
    return distances