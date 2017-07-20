#! /usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
from arcpy.sa import *
# Description: Extracts the cells of a raster that correspond with the areas
#    defined by a mask.
# Requirements: Spatial Analyst Extension

# Import system modules
# Set environment settings
#第二步：按掩膜提取
# Description: Extracts the cells of a raster that correspond with the areas
# defined by a mask.
# Requirements: Spatial Analyst Extension
# Set local variables
env.workspace = "E:/work_SIC/201706/light_index_workspace"
inRaster = "SVDNB_npp_20160901-20160930_75N060E_vcmcfg_v10_c201610280941/SVDNB_npp_20160901-20160930_75N060E_vcmcfg_v10_c201610280941.avg_rade9.tif"
inMaskData = "pyIO/mzsg_py1"
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")
# Execute ExtractByMask
outExtractByMask = ExtractByMask(inRaster, inMaskData)
# Save the output
outExtractByMask.save("E:/work_SIC/201706/light_index_workspace/pyIO/aymtq1")
