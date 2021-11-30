import geopandas as gpd

def main(pathToLanduse, pathToSoil, pathToHru, levelOfDetail):
    """
    Builds spatial subsets based on the land use and soil shape features

    Keyword-arguments
    pathToLanduse -- total path to the land use layer
    pathToSoil -- total path to soil layer
    pathToHru -- total path where the produced hru layer will be written
    levelOfDetail -- level of detail for the land use layer. Either use "HG", "UG", "Bestand"
    """

    ## prepare land use layer
    landuse = gpd.read_file(pathToLanduse)

    if levelOfDetail == "HG":
        uniqueColumn = landuse.HG.astype(str)
    if levelOfDetail == "UG":
        uniqueColumn = landuse.HG.astype(str) + landuse.UG.astype(str)
    if levelOfDetail == "Bestand":
        uniqueColumn = landuse.HG.astype(str) + landuse.UG.astype(str) + landuse.BESTAND.astype(str)

    landuse["unique"] = uniqueColumn
    landuseReduced = landuse.dissolve(by = "unique", as_index= False)
    landuseReduced.drop(landuseReduced.columns.difference(['unique','geometry']), 1, inplace=True)

    ## prepare soil layer
    soil = gpd.read_file(pathToSoil)
    soilReduced = soil.dissolve(by = "BOTYP", as_index= False)
    soilReduced.drop(soilReduced.columns.difference(['BOTYP','geometry']), 1, inplace=True)

    ## create HRUs
    hru = soilReduced.overlay(landuseReduced, how='union')
    hruContiguous = hru.explode(index_parts=True)
    hruContiguous.to_file(pathToHru)
