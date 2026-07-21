import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def plot_accessibility_choropleth(
    polygons: gpd.GeoDataFrame,
    pois: gpd.GeoDataFrame,
    weighted_accessibility: pd.Series,
    title: str,
    n_classes: int,
    output_path: str = "reports/accessibility_map.png",
) -> None:
    """
    Renders a choropleth map showing spatial-justice accessibility per district, and saves it as a PNG.

    Args:
        polygons: GeoDataFrame with district geometries
        weighted_accessibility: Series from weight_accessibility
        title: map title
        n_classes: number of quantile classes for the color scale
        output_path: where to save the PNG        
    """
    # Merge the score with polygons
    map_data = polygons.copy()
    map_data["accessibility_score"] = weighted_accessibility

    pois_data = pois.copy()

    if pois_data.crs != map_data.crs:
       logger.info(f"Reprojecting POIs from {pois_data.crs} to {map_data.crs} for plotting")
       pois_data = pois_data.to_crs(map_data.crs)
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 10))

    map_data.plot(
        column="accessibility_score",
        cmap="YlOrRd",            
        scheme="quantiles",          
        k=n_classes,
        legend=True,
        legend_kwds={
            "title": "Índice de privación de acceso\n(más alto = peor acceso)",
            "loc": "lower right",
            "fontsize": 8,
        },
        edgecolor="grey",
        linewidth=0.5,
        missing_kwds={
            "color": "lightgrey",
            "label": "Sin datos",
        },
        ax=ax,
    )

    pois_data.plot(
        ax=ax,
        color="blue",
        marker="^",
        markersize=80,
        edgecolor="blue",
        linewidth=1,
        label="Points of interest",
        zorder=3,  
    )

    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_axis_off()
    ax.legend(loc="upper left", fontsize=8, frameon=True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Choropleth map saved to {output_path}")