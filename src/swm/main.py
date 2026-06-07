import logging
import sys
import matplotlib.pyplot as plt
from swm.io import load_geodata


logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def main():
    logger.info("SWM Explorer. Starting Execution")
    
    gdf = load_geodata("upl.geojson")
    logger.info(f"Loaded: {gdf.shape[0]} features")
    print(list(gdf))
    hei = load_geodata("ies.geojson") ## high education institution
    logger.info(f"Loaded: {hei.shape[0]} features")
    

if __name__ == "__main__":
    main()