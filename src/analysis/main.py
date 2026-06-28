import logging
import sys
import typer
import time
import sys
from analysis.io import load_geodata, load_weighting_config
from analysis.network import get_centroids, get_bbox_wgs84, download_network, build_pandana_network
from analysis.pois import register_pois
from analysis.accessibility import compute_accessibility
from analysis.socioeconomic import weight_accessibility, normalize_variables


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

app = typer.Typer()

@app.command()
def main(
    polygons_file: str = typer.Option(
        "data.geojson",
        "--polygons",
        "-pl",
        help="GeoJSON filename for the polygons (e.g. District or neighbors boundaries).",
    ),
    config_file: str = typer.Option(
        "config.csv",
        "--config",
        "-c",
        help="CSV filename with socioeconomic variables that want to be included in the analysis and its weights (e.g. District or neighbors boundaries).",
    ),
    points_file: str = typer.Option(
        "ies.geojson",
        "--points",
        "-pt",
        help="GeoJSON filename for the points (e.g. Higher Education Institutions).",
    ),
    network_type: str = typer.Option(
        "drive",
        "--network_type",
        "-n",
        help="From OSMmnx, the options available are: all, all_public, bike, drive, drive_service, walk.",
    ),
    max_distance: float = typer.Option(
        20000,
        "--max_distance",
        "-md",
        help="The maximum distance that will be used to find all the nearest pois"
    ),
    max_items: int = typer.Option(
        10,
        "--max_items",
        "-mi",
        help="The maximum number of items that will be found"
    ), num_pois: int = typer.Option(
        5,
        "--num_pois",
        "-np",
        help="Count of POIs reachable within the maximum distance"
    ), 
):
    logger.info("Accessibility Explorer. Starting Execution")
    start = time.time()

    # -----------------------------------------
    # --- Read data and configuration files ---
    # -----------------------------------------

    polygons = load_geodata(polygons_file)
    logger.info(f"Loaded: {polygons.shape[0]} features")
    pois = load_geodata(points_file, reproject_to=4326) 
    logger.info(f"Loaded: {pois.shape[0]} features")

    all_vars = load_weighting_config(config_file=config_file)

    normalize_variables(polygons, all_vars)

    sys.exit(0)
    # -------------------------------------------------------------------------- 
    # --- Get the distance from the centroids to the nearest 10 institutions ---
    # -------------------------------------------------------------------------- 

    # --- Get the centroids of the polygons ---
    centroids = get_centroids(polygons)
    logger.info(f"Calculated: {centroids.shape[0]} centroids")

    # --- Get the bbox of the polygons ---
    bbox = get_bbox_wgs84(polygons)
    logger.info(f"Bounding box is {bbox}")
    # --- Build the graph for that bbox ---
    graph   = download_network(bbox, network_type=network_type)
    # --- Building the network using the graph ---
    network = build_pandana_network(graph)
    # --- Register pois in the network ---
    register_pois(network, pois, max_distance=max_distance, max_items=max_items)
    # print(network.nodes_df.head())

    raw_accessibility = compute_accessibility(network, max_distance=max_distance, num_pois=num_pois)
    raw_accessibility.head()

    weighted_accessibility = weight_accessibility(polygons, all_vars)


    end = time.time()
    logger.info(f"Execution time: {end - start:.2f} seconds")

if __name__ == "__main__":
    app()