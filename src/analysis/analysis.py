import geopandas as gpd

def count_ies_in_polygons(polygons, points):
    
    points_inside_polygons = gpd.sjoin(polygons, points)

    points_count = points_inside_polygons.groupby("CODIGO_UPL").size().reset_index(name="points_count")

    polygons = polygons.merge(points_count, on="CODIGO_UPL", how="left")
    polygons["points_count"] = polygons["points_count"].fillna(0)

    return polygons

def get_centroids(polygons):
    centroid = polygons.geometry.centroid
    return centroid