#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      matt.worthy
#
# Created:     16/03/2018
# Copyright:   (c) matt.worthy 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy

fc = r"C:\Emily\CDO26\Deliverables\UGA\FGCM_CDO26_TDS_v61_UGA_Ancillary_sub1\Imagery_Footprints\CDO26_UGA_20181206_Footprints.shp"

dates = []
with arcpy.da.SearchCursor(fc, "Acquisitio") as sCursor:
    for sRow in sCursor:
        if sRow[0] not in dates:
            dates.append(sRow[0])

print sorted(dates, reverse=True)



dates_sorted = sorted(dates, reverse=True)


fc_temp = "in_memory/fc_temp"
queryBase = """"Acquisitio" = date '{}'""".format(dates_sorted[0])
arcpy.Select_analysis(fc, fc_temp, queryBase)
print "BASE = {}".format(int(arcpy.GetCount_management(fc_temp).getOutput(0)))

lyr = "lyr"
erase_temp = "in_memory/erase_temp"
for dt in dates_sorted[1:]:
    print dt
    arcpy.MakeFeatureLayer_management(fc, lyr, """"Acquisitio" = date '{}'""".format(dt))
    print"  selection = {}".format(int(arcpy.GetCount_management(lyr).getOutput(0)))
    arcpy.Erase_analysis(lyr, fc_temp, erase_temp)
    if arcpy.Exists(erase_temp):
        print"  erased = {}".format(int(arcpy.GetCount_management(erase_temp).getOutput(0)))
        if int(arcpy.GetCount_management(erase_temp).getOutput(0)) > 0:
            arcpy.Append_management(erase_temp, fc_temp, "NO_TEST")
            print "  fc_temp = {}".format(int(arcpy.GetCount_management(fc_temp).getOutput(0)))
        arcpy.Delete_management(erase_temp)
    arcpy.Delete_management(lyr)


fc_final = fc.split(".shp")[0]+"_planarized.shp"
arcpy.Select_analysis(fc_temp, fc_final)

arcpy.Delete_management("in_memory")
