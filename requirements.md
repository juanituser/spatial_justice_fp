# Requirements

1. Calculate physical distance from each polygon to the closest HEI

   - Calculate centroid of each UPL polygon (in WGS84 for pandana compatibility)
   - Snap each centroid to the nearest node in the street network using 
   - For each node, query to get distances to the N nearest HEIs
   - Take the mean of those N distances per UPL as the baseline physical accessibility score

2. Weight the physical distance by socioeconomic and subjective variables

   - Read and save in a df the csv file with variables to include and its weights
   - Normalize all weighting variables (income, satisfaction with neighborhood, satisfaction with life) to a 0-1 scale so they are comparable 
   - Build a composite factor from those normalized variables, weighted according user wants to
   - Structure variables as impedance to include in pandana **network.nearest_pois**
   - The result is the composite accessibility indicator: a weighted distance that reflects not only how far a district is from higher educational institutios but how hard that distance is given its socioeconomic and perceptual conditions

3. Map the result

   - Plot a choropleth map of the composite accessibility indicator across UPLs, where UPLs with higher values face greater structural barriers to accessing higher education