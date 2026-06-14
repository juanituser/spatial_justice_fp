import pandana
import pandas as pd

def compute_accessibility(
    network: pandana.Network,
    max_distance: float,
    num_pois: int
) -> pd.DataFrame:

    print(f"Precomputing network reachability up to {max_distance}m...")
    network.precompute(max_distance)

    distances = network.nearest_pois(
    distance=max_distance,
    category="poi",
    num_pois=num_pois
    )

    print(distances)

    mean_distance = distances.mean(axis=1)

    return distances