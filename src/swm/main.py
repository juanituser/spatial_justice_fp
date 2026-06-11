import logging
import sys
import typer
from swm.io import load_geodata
from swm.network import get_centroids, get_bbox_wgs84
 

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
):
    logger.info("Accessibility Explorer. Starting Execution")
    
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

if __name__ == "__main__":
    app()