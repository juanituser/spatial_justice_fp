import logging
import sys
from swm.io import load_database
from swm.weights import create_rook_swm, create_queen_swm, create_distance_swm, create_knn_swm, create_socio_swm

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s -%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def main():
    logger.info("SWM Explorer. Starting Execution")
    
    polygons = load_database()
    # print(polygons.head())

    # rook_w = create_rook_swm(polygons)
    queen_w = create_queen_swm(polygons)
    knn_w = create_rook_swm(polygons)
    distance_band_w = create_queen_swm(polygons)
    example = create_socio_swm(polygons, queen_w, "pct_welfare_15_64")

    ##### CREATE VISUALIZATION

    # print(distance_band_w.weights)
    # print(queen_w.weights)
    print(example.weights)


if __name__ == "__main__":
    main()