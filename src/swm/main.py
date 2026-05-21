import logging
import sys
import matplotlib.pyplot as plt
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
    
    upl = load_geodata("upl.geojson")
    hei = load_geodata("ies.geojson")
    
    get_bounding_box(upl)
    get_bounding_box(hei)
    fig, ax = plt.subplots()   
    upl.plot(ax=ax, color="lightgrey", edgecolor="white", linewidth=0.5)
    hei.plot(ax=ax, color="steelblue", markersize=3)
    ax.set_axis_off()
    plt.show()

    

if __name__ == "__main__":
    main()