import logging
import sys
import typer
from swm.io import load_geodata
from swm.analysis import count_ies_in_polygons
from swm.viz import plot_choropleth
from swm.network import get_bbox_wgs84



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
    )
):
    logger.info("SWM Explorer. Starting Execution")
    
    polygons = load_geodata(polygons_file, reproject_to=reproject_to)
    logger.info(f"Loaded: {polygons.shape[0]} features")
    hei = load_geodata(points_file, reproject_to=reproject_to) 
    logger.info(f"Loaded: {hei.shape[0]} features")

    # districts = count_ies_in_polygons(polygons, hei)

    # plot_choropleth(districts, column="points_count", title="IES por UPL")

    ##Analysis
    
    # --- Build all W matrices ---
    get_bbox_wgs84(polygons)


if __name__ == "__main__":
    app()