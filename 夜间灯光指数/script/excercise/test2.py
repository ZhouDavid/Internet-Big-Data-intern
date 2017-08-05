# connect to ArcGIS Online
import pandas as pd
import numpy as np
from arcgis.gis import GIS
from arcgis.geoprocessing import import_toolbox

gis = GIS()
chinaMap = gis.content.search('China')
chinaCities = gis.content.search()

