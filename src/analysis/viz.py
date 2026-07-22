import logging
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import geopandas as gpd
import pandas as pd
import mapclassify
from pathlib import Path


logger = logging.getLogger(__name__)

def plot_accessibility_choropleth(
    polygons: gpd.GeoDataFrame,
    pois: gpd.GeoDataFrame,
    accessibility_score: pd.Series,
    title: str,
    weighted: bool = True,
    n_classes: int = 5,
    subtitle: str | None = None,
):
    """
    Renders a choropleth map with an explicit class legend and POI locations, and saves it as a PNG.

    Args:
        accessibility_score: Series indexed like `polygons`. Higher = worse access. Pass either the raw accessibility or the socioeconomically weight accessibility.
    """
    map_data = polygons.copy()
    map_data["accessibility_score"] = accessibility_score

    missing = map_data["accessibility_score"].isna()
    if missing.any():
        logger.warning(
            f"{missing.sum()} districts have no accessibility score "
            f"and will appear blank: {map_data.loc[missing].index.tolist()}"
        )

    valid_scores = map_data["accessibility_score"].dropna()
    classifier = mapclassify.Quantiles(valid_scores, k=n_classes)
    map_data["class"] = classifier.yb

    class_labels = [
        "Excellent accessibility",
        "Good accessibility",
        "Medium accessibility",
        "Low accessibility",
        "Needs priority attention",
    ]

    if subtitle is None:
        subtitle = (
            "Socioeconomically weighted accessibility deprivation index by district"
            if weighted
            else "Raw accessibility (distance to nearest POIs) by district"
        )

    legend_title = "Accessibility level (weighted)" if weighted else "Accessibility level (raw distance)"

    fig, ax = plt.subplots(figsize=(11, 11))

    map_data.plot(
        column="class",
        cmap="YlOrBr",
        categorical=True,
        edgecolor="#999999",
        linewidth=0.4,
        alpha=0.85,
        missing_kwds={"color": "#eeeeee"},
        ax=ax,
        legend=False,
    )

    pois.plot(
        ax=ax, color="black", marker="o", markersize=35,
        edgecolor="white", linewidth=0.6, zorder=4,
    )

    cmap = plt.get_cmap("YlOrBr", n_classes)
    legend_patches = [
        mpatches.Patch(color=cmap(i), label=class_labels[i], alpha=0.85)
        for i in range(n_classes)
    ]
    poi_marker = plt.Line2D(
        [0], [0], marker="o", color="w", markerfacecolor="black",
        markersize=8, markeredgecolor="white", label="Points of interest"
    )
    ax.legend(
        handles=legend_patches + [poi_marker],
        loc="lower right", fontsize=9, title=legend_title,
        title_fontsize=10, frameon=True, facecolor="white", framealpha=0.9,
    )

    ax.set_title(title, fontsize=16, fontweight="bold", pad=25)
    ax.text(0.5, 1.01, subtitle, transform=ax.transAxes, ha="center", fontsize=11, color="dimgrey")

    ax.set_axis_off()

    output_path = "reports/accessibility_map_weighted.png" if weighted else "reports/accessibility_map_raw.png"
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)

    logger.info(f"Choropleth map saved to {output_path} (weighted={weighted})")