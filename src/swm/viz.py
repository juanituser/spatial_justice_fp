import matplotlib.pyplot as plt


def plot_choropleth(polygons, column, title):

    """
    Visualizes a cloropleth map using the indicated column.
    Use this for the showing possible spatial relation.
    """

    fig, ax = plt.subplots(figsize=(10, 10))

    polygons.plot(
        column=column,
        cmap="YlOrRd",
        legend=True,
        ax=ax
    )

    # hei.plot(ax=ax, color="blue", markersize=3, label="IES")

    ax.set_axis_off()
    plt.title(title)
    plt.show()

    return fig

# def plot_swm_weighted(gdf, w, title: str):
#     """
#     Visualizes a weighted W object — line thickness encodes edge weight.
#     Use this for the socioeconomic W to show varying connection strength.
#     """
#     fig, ax = plt.subplots(figsize=(8, 8))
#     gdf.plot(ax=ax, color="lightgrey", edgecolor="white", linewidth=0.5)

#     centroids = gdf.geometry.centroid
#     cx = centroids.x.values
#     cy = centroids.y.values

#     # collect all weights to normalize line thickness across the full range
#     all_weights = [weight for weights in w.weights.values() for weight in weights]
#     max_weight = max(all_weights)
#     min_weight = min(all_weights)
#     weight_range = max_weight - min_weight if max_weight != min_weight else 1.0

#     for i, neighbors in w.neighbors.items():
#         for j, weight in zip(neighbors, w.weights[i]):
#             # normalize weight to [0, 1] relative to the actual range in this W
#             normalized = (weight - min_weight) / weight_range
#             contrast = normalized ** 2
#             # I tweeked the contrast, and linewidth on purpuse
#             ax.plot(
#                 [cx[i], cx[j]],
#                 [cy[i], cy[j]],
#                 color="steelblue",
#                 linewidth=0.3 + contrast * 12,
#                 alpha=0.15 + contrast * 0.85,
#             )

#     ax.scatter(cx, cy, color="steelblue", s=15, zorder=3)
#     ax.set_title(title)
#     ax.set_axis_off()
#     return fig