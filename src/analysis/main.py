import logging
import sys
import typer
import time
from analysis.io import load_geodata, load_weighting_config
from analysis.network import get_centroids, get_bbox_wgs84, download_network, build_pandana_network
from analysis.pois import register_pois
from analysis.accessibility import compute_accessibility
from analysis.socioeconomic import weight_accessibility
from analysis.viz import plot_accessibility_choropleth

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
        "munster_dummy.geojson",
        "--polygons",
        "-pl",
        help="GeoJSON filename for the polygons (e.g. District or neighbors boundaries).",
    ),
    config_file: str = typer.Option(
        "config_munster.csv",
        "--config",
        "-c",
        help="CSV filename with socioeconomic variables that want to be included in the analysis and its weights (e.g. District or neighbors boundaries).",
    ),
    points_file: str = typer.Option(
        "heis_munster.geojson",
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
        100000,
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
    ), title: str = typer.Option(
        'Accesibiity Map',
        "--title",
        "-t",
        help="Title of the report"
    ), n_classes: int = typer.Option(
        5,
        "--n_classes",
        "-nc",
        help="Number of classes to create the cloropleth map"
    ),


):
    logger.info("Accessibility Explorer. Starting Execution")
    start = time.time()

    # -----------------------------------------
    # --- Read data and configuration files ---
    # -----------------------------------------

    polygons = load_geodata(polygons_file)
    logger.info(f"Loaded: {polygons.shape[0]} features")
    pois = load_geodata(points_file, reproject_to=4326) ### IN THIS CASE, HEI
    logger.info(f"Loaded: {pois.shape[0]} features")

    all_vars = load_weighting_config(config_file=config_file)

    # -------------------------------------------------------------------------- 
    # --- Get the distance from the centroids to the nearest 10 institutions ---
    # -------------------------------------------------------------------------- 

    # --- Get the centroids of the polygons ---
    centroids = get_centroids(polygons)
    
    # --- Get the bbox of the polygons ---
    bbox = get_bbox_wgs84(polygons)
    logger.info(f"Bounding box is {bbox}")
    # --- Build the graph for that bbox ---
    graph   = download_network(bbox, network_type=network_type)
    # --- Building the network using the graph ---
    network = build_pandana_network(graph)

    # --- Register pois in the network ---
    register_pois(network, pois, max_distance=max_distance, max_items=max_items)

    # --- Calculate accessibility from each polygon to each POI --- 
    raw_accessibility = compute_accessibility(network, centroids, max_distance=max_distance, num_pois=num_pois)
    
    # --- Calculate weighted accessibility including distances and external variables and its direction --- 
    weighted_accessibility = weight_accessibility(raw_accessibility, polygons, all_vars)
    
    # --- Visualization --- 

    plot_accessibility_choropleth(polygons, pois, accessibility_score=raw_accessibility["mean_dist"],
    title="Raw Accessibility to Points of Interest", weighted=False)

    plot_accessibility_choropleth(polygons, pois, accessibility_score=weighted_accessibility,     title="Weighted Accessibility to Points of Interest", weighted=True)

    end = time.time()
    logger.info(f"Execution time: {end - start:.2f} seconds")

if __name__ == "__main__":
    app()