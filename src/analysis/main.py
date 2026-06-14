import logging
import sys
import typer
import time
from analysis.io import load_geodata
from analysis.network import get_centroids, get_bbox_wgs84, download_network, build_pandana_network
from analysis.pois import register_pois
 

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
        10000,
        "--max_distance",
        "-md",
        help="The maximum distance that will be used to find all the nearest pois"
    ),
    max_items: int = typer.Option(
        10,
        "--max_items",
        "-mi",
        help="The maximum number of items that will be found"
    )
):
    logger.info("Accessibility Explorer. Starting Execution")
    start = time.time()

    polygons = load_geodata(polygons_file)
    logger.info(f"Loaded: {polygons.shape[0]} features")
    pois = load_geodata(points_file, reproject_to=4326) 
    logger.info(f"Loaded: {pois.shape[0]} features")

    print(polygons.crs)          
    print(polygons.shape)       
    print(pois.crs)                 
    print(pois.shape)    

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
    print(network.nodes_df.head())

    end = time.time()
    logger.info(f"Execution time: {end - start:.2f} seconds")

if __name__ == "__main__":
    app()