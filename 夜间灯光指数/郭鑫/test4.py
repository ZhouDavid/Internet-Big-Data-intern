# Name: TableToExcel_2.py

import arcpy

# Set environment settings
arcpy.env.workspace = "E:/work_SIC/201706/light_index_workspace"

# Set local variables
in_table = "pyIO/qyfx1.dbf"
out_xls = "pyIO/output.xls"

# Execute TableToExcel
arcpy.TableToExcel_conversion(in_table, out_xls)

