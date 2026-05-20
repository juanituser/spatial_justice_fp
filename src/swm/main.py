import logging
import sys
from swm.io import load_geodata
from swm.boundingbox import get_bounding_box


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def main():
    logger.info("SWM Explorer. Starting Execution")
    
    upl = load_geodata("upl.geojson", reproject_to=4686)
    hei = load_geodata("ies.geojson", reproject_to=4686)
    
    get_bounding_box(upl)
    get_bounding_box(hei)

if __name__ == "__main__":
    main()