#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Import system modules
import arcpy
from arcpy import env

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


