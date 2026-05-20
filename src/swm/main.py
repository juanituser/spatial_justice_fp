import logging
import sys
from swm.io import load_geodata


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def main():
    logger.info("SWM Explorer. Starting Execution")
    
    upl = load_geodata("upl.json", reproject_to=4686)
    hei = load_geodata("ies.geojson", reproject_to=4686)
    
    print(upl.head())
    print(hei.head())

if __name__ == "__main__":
    main()