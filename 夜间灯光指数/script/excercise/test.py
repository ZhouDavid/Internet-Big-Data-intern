from arcgis.gis import GIS
gis = GIS()

# search and list all feature layers in my contents
search_result = gis.content.search(query="", item_type="Feature Layer")
print(search_result)