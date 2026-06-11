import logging
import sys
import typer
import time
from analysis.io import load_geodata
from analysis.network import get_centroids, get_bbox_wgs84, download_network, build_pandana_network
 

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
        "-p",
        help="GeoJSON filename for the polygons (e.g. District or neighbors boundaries).",
    ),
    points_file: str = typer.Option(
        "ies.geojson",
        "--points",
        "-pt",
        help="GeoJSON filename for the points (e.g. Higher Education Institutions).",
    ),
    reproject_to: int = typer.Option(
        "3116",
        "--reproject-to",
        "-r",
        help="EPSG code to reproject both layers.",
    ),
    network_type: str = typer.Option(
        "drive",
        "--network_type",
        "-n",
        help="From OSMmnx, the options available are: all, all_public, bike, drive, drive_service, walk.",
    ),
):
    logger.info("Accessibility Explorer. Starting Execution")
    start = time.time()

    polygons = load_geodata(polygons_file, reproject_to=reproject_to)
    logger.info(f"Loaded: {polygons.shape[0]} features")
    hei = load_geodata(points_file, reproject_to=reproject_to) 
    logger.info(f"Loaded: {hei.shape[0]} features")

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
    

    end = time.time()
    logger.info(f"Execution time: {end - start:.2f} seconds")

if __name__ == "__main__":
    app()