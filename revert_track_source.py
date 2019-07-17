import arcpy

def msg(message):
    arcpy.AddMessage(message)
    print message

def warn(message):
    arcpy.AddWarning(message)
    print message

def error(message):
    arcpy.AddError(message)
    print message

current = r"C:\Emily\CDO26\QC\DZA\DZA_6\DZA_6_QCFinal.gdb"
source = r"C:\Emily\CDO26\QC\DZA\SOURCE\Baseline_Data\CDO42_DZA_Zone_6_20181023.gdb"
missing_field = "ZI001_SDP = 'No Information'"
trans_lyr = "trans_lyr"
arcpy.env.workspace = source

## rename source fc
arcpy.Rename_management("TransportationGroundCrv", "TransportationGroundCrv_source", "FeatureClass")
source_new = source + "\TDS\TransportationGroundCrv_source"


## create layer from sdp = no info
arcpy.env.workspace = current
arcpy.MakeFeatureLayer_management("TransportationGroundCrv", trans_lyr, missing_field)


## join to source
arcpy.AddJoin_management (trans_lyr, "hc_GlobalID", source_new, "hc_GlobalID")


## field calc to pull over original attribution
print "Reverting metadata attribution back to original..."
            ######current_fieldNames = ["zi001_srt", "zi001_sdv", "zi001_sdp", "ccn", "zsax_rs0", "zsax_rx0", "zsax_rx3"]
            ######source_fieldNames = ["ZI001_SRT", "ZI001_SDV", "ZI001_SDP", "CCN", "ZSAX_RS0", "ZSAX_RX0", "ZSAX_RX3"]
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.ZI001_SRT", "!TransportationGroundCrv_source.ZI001_SRT!", "PYTHON_9.3")
print "SRT reverted"
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.ZI001_SDV", "!TransportationGroundCrv_source.ZI001_SDV!", "PYTHON_9.3")
print "SDV reverted"
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.ZI001_SDP", "!TransportationGroundCrv_source.ZI001_SDP!", "PYTHON_9.3")
print "SDP reverted"
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.CCN", "!TransportationGroundCrv_source.CCN!", "PYTHON_9.3")
print "CCN reverted"
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.ZSAX_RS0", "!TransportationGroundCrv_source.ZSAX_RS0!", "PYTHON_9.3")
print "RS0 reverted"
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.ZSAX_RX0", "!TransportationGroundCrv_source.ZSAX_RX0!", "PYTHON_9.3")
print "RX0 reverted"
arcpy.CalculateField_management(trans_lyr, "TransportationGroundCrv.ZSAX_RX3", "!TransportationGroundCrv_source.ZSAX_RX3!", "PYTHON_9.3")
print "RX3 reverted"


## delete lyr
arcpy.Delete_management(trans_lyr)

## rename source back to original
arcpy.env.workspace = source
arcpy.Rename_management("TransportationGroundCrv_source", "TransportationGroundCrv", "FeatureClass")


