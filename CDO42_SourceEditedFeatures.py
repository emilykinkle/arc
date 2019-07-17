#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      matt.worthy
#
# Created:     15/05/2018
# Copyright:   (c) matt.worthy 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import arcpy
from datetime import datetime

def msg(message):
    arcpy.AddMessage(message)
    print message

def warn(message):
    arcpy.AddWarning(message)
    print message

def error(message):
    arcpy.AddError(message)
    print message

gdb = r"C:\Emily\CDO26\Deliverables\UGA\FGCM_CDO26_TDS_v61_UGA_sub1\UGA_1_TDS.gdb" #
imagery_footprints = r"C:\Emily\CDO26\Deliverables\UGA\FGCM_CDO26_TDS_v61_UGA_Ancillary_sub1\Imagery_Footprints\CDO26_UGA_20181206_Footprints_planarized.shp" #
arcpy.env.workspace = gdb
qc_DoNotUpdate = "false" #arcpy.GetParameterAsText(2) #

ignoreFCs = ('MetadataSrf', 'ResourceSrf')
sourceFields = ['ZI001_SRT', 'ZI001_SDV', 'ZI001_SDP', 'CCN', 'ZSAX_RS0', 'ZSAX_RX0', 'ZSAX_RX3']

dg_SRT = "imageryUnspecified"
dg_SDP = "DigitalGlobe"
dg_CCN = "Copyright 2018 by the National Geospatial-Intelligence Agency, U.S. Government. No domestic copyright claimed under Title 17 U.S.C. All rights reserved."
dg_RS0 = "U"
dg_RX0 = "FOUO"
dg_RX3 = "No Information"


footprints_lyr = "footprints_lyr"
arcpy.MakeFeatureLayer_management(imagery_footprints, footprints_lyr)

for fc in arcpy.ListFeatureClasses("*", "All", "TDS"):
    msg(fc)
    if fc not in ignoreFCs and int(arcpy.GetCount_management(fc).getOutput(0)) > 0:

        query_general_20180515 = "((ZI001_SDV LIKE '2019%' OR ZI001_SDV LIKE '2018-12-%') OR (ZI001_SDV = 'noInformation' AND ZI001_SDP = 'DigitalGlobe') OR (ZI001_SDP IN ('noInformation', 'NoInformation', 'No Information', '-999999', 'Digital Globe')))"
        laf_FCs = ("AgricultureSrf", "PhysiographySrf", "VegetationSrf")
        query_LAF_20180515 = query_general_20180515+" AND ZI001_SDP IN ('noInformation', 'NoInformation', 'No Information', '-999999', 'Digital Globe')"

        fc_lyr = "fc_lyr"
        if fc in laf_FCs:
            arcpy.MakeFeatureLayer_management(fc, fc_lyr, query_LAF_20180515)
        else:
            arcpy.MakeFeatureLayer_management(fc, fc_lyr, query_general_20180515)

        if int(arcpy.GetCount_management(fc_lyr).getOutput(0)) > 0:
            arcpy.SelectLayerByLocation_management(footprints_lyr, "INTERSECT", fc_lyr, "0 Meters", "NEW_SELECTION")

            if int(arcpy.GetCount_management(footprints_lyr).getOutput(0)) > 0:
                with arcpy.da.SearchCursor(footprints_lyr, ["FID", "Acquisitio"]) as sCursor:
                    for sRow in sCursor:
                        fid = sRow[0]
                        formatedDate = datetime.strftime(sRow[1], "%Y-%m-%d")


                        sel_lyr="sel_lyr"
                        update_lyr = "update_lyr"
                        arcpy.MakeFeatureLayer_management(footprints_lyr, sel_lyr, '"FID" = {}'.format(fid))
                        arcpy.MakeFeatureLayer_management(fc_lyr, update_lyr)
                        arcpy.SelectLayerByLocation_management(update_lyr, "HAVE_THEIR_CENTER_IN", sel_lyr, "0 Meters", "NEW_SELECTION")

                        if int(arcpy.GetCount_management(update_lyr).getOutput(0)) > 0:

##                            arcpy.DisableEditorTracking_management(fc, "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")

                            count = 0
                            with arcpy.da.UpdateCursor(update_lyr, sourceFields) as uCursor:
                                for uRow in uCursor:
                                    if qc_DoNotUpdate != 'true':
                                        uRow[0] = dg_SRT
                                        uRow[1] = formatedDate
                                        uRow[2] = dg_SDP
                                        uRow[3] = dg_CCN
                                        uRow[4] = dg_RS0
                                        uRow[5] = dg_RX0
                                        uRow[6] = dg_RX3
                                        uCursor.updateRow(uRow)
                                    count +=1

##                            arcpy.EnableEditorTracking_management(fc, "created_user", "created_date", "last_edited_user", "last_edited_date")

                            if count > 0:
                                if qc_DoNotUpdate != 'true':
                                    warn("  {} features updated to {}".format(count, formatedDate))
                                else:
                                    warn("  Features to be Updated: {}".format(count))


                        arcpy.Delete_management(sel_lyr)
                        arcpy.Delete_management(update_lyr)
        arcpy.Delete_management(fc_lyr)
arcpy.Delete_management(footprints_lyr)
