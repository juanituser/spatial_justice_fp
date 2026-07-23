# Requirements

1. Calculate physical distance from each polygon to the closest POI

   - Calculate centroid of each districts polygon (in WGS84 for pandana compatibility)
   - Snap each centroid to the nearest node in the street network using 
   - For each node, query to get distances to the N nearest POIs
   - Take the mean of those N distances per districts as the baseline physical accessibility score

2. Weight the physical distance by socioeconomic and subjective variables

   - Read and save in a df the csv file with variables to include and its weights
   - Normalize all weighting variables to a 0-1 scale so they are comparable and include their direction
   - Build a composite factor from those normalized variables, weighted according user wants to and distance (raw inaccessibility score)
   - The result is the composite accessibility indicator: a weighted distance that reflects not only how far a district is from higher educational institutios but how hard that distance is given its socioeconomic and perceptual conditions

3. Map the result

   - Plot a choropleth map of the composite accessibility indicator across districts, where districts with higher values face greater structural barriers to accessing certain Point of Interest.