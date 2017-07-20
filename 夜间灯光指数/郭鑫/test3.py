#! /usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
from arcpy.sa import *
# Name: ZonalStatisticsAsTable_Ex_02.py
# Description: Summarizes values of a raster within the zones of
#              another dataset and reports the results to a table.
# Requirements: Spatial Analyst Extension

#第三步：以表格显示分区统计
# Description: Summarizes values of a raster within the zones of another dataset and reports the results to a table.
# Requirements: Spatial Analyst Extension
# Set local variables
env.workspace = "E:/work_SIC/201706/light_index_workspace"
inZoneData = "country_line/albers.shp"
zoneField = "LEVEL3_"
inValueRaster = "pyIO/aymtq1"
outTable = "pyIO/qyfx1.dbf"
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Execute ZonalStatisticsAsTable
outZSaT = ZonalStatisticsAsTable(inZoneData, zoneField, inValueRaster, outTable, "NODATA", "MEAN")
