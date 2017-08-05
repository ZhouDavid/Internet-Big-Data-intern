from arcgis.gis import GIS
import arcgis.geoanalytics

gis = GIS("https://python.playground.esri.com/portal", "arcgis_python", "amazing_arcgis_123")
dataManager = arcgis.geoanalytics.get_datastores()
bigFiles=dataManager.search()
# print(bigFiles)
secondData = dataManager.add_bigdata('secondData',r'E:\\互联网大数据分析家中心实习\\data')
print(secondData.manifest)

# search_result = gis.content.search("", item_type = "big data file share")
# print(search_result)