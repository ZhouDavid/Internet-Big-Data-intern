#! /usr/bin/env python
# -*- coding: utf-8 -*-

import arcpy
from arcpy import env
from arcpy.sa import *
import datetime

#记录程序开始时间
starttime = datetime.datetime.now()
print starttime


# 设置工作环境
env.workspace = "E:/work_SIC/201706/light_index_workspace"

#第一步：面转栅格，把县级行政区域信息albers.shp转为栅格数据，精度可以高一些（像元大小<=500）
# Description: Converts polygon features to a raster dataset.
# Set local variables
inFeatures = "country_line/albers.shp"   #面的名称
valField = "LEVEL3_"
outRaster = "E:/work_SIC/201706/light_index_workspace/pyIO/mzsg_py1"  #输出栅格数据集的文件夹
assignmentType = "CELL_CENTER"
priorityField = "NONE"
cellSize = 100               #像元大小
# Execute PolygonToRaster
arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, assignmentType, priorityField, cellSize)

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

#第四步：以表格的形式输出文件
# Set local variables
env.workspace = "E:/work_SIC/201706/light_index_workspace"
in_table = "pyIO/qyfx1.dbf"
out_xls = "pyIO/output666.xls"
# Execute TableToExcel
arcpy.TableToExcel_conversion(in_table, out_xls)


#记录程序结束时间
endtime = datetime.datetime.now()
print endtime
print (endtime - starttime).seconds