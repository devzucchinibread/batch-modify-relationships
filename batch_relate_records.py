import arcpy
import gis_utils as gu


# Params

service_layers = arcpy.GetParameter(0)  # Layer from TOC
woh_globalid = arcpy.GetParameterAsText(1)  # WOH GlobalID as string
proceed_if_none = arcpy.GetParameterAsText(2)  # "Yes" or "No"
action_type = arcpy.GetParameterAsText(3) #Add/Remove

def modify_relationships(service_layer):

    arcpy.AddMessage("Modifying {}".format(service_layer))

    # Input selected features
    selected_ids = []
    with arcpy.da.SearchCursor(service_layer, ["OBJECTID"]) as cursor:
        for row in cursor:
            selected_ids.append(row[0])

    # make sure there are selected feature
    if len(selected_ids) == 0:
        arcpy.AddWarning("No features are selected. The tool will apply to ALL features in the layer.")
        if proceed_if_none.lower() != "yes":
            arcpy.AddMessage("Tool canceled by user.")
            raise SystemExit()



    #Get the Root SDE path
    sde_path = gu.get_sde_path(layer)


    #Target the Relationship Class Based On the Keyword (In my demo example I used WOH)
    rel_class = gu.find_rel(layer, "WorkOrderHistory")



    keys = gu.get_rc_keys(rel_class)
    arcpy.AddMessage("RC table Keys:{}".format(keys))



    #--- START EDIT SESSION (REQUIRED FOR RELATIONSHIP INSERT) ---
    edit = arcpy.da.Editor(sde_path)
    edit.startEditing(False, True)
    edit.startOperation()
    arcpy.AddMessage("Edit Session Initatied in: {}".format(sde_path))

    #3try:
    if action_type == "Add relationships":
        # --- RELATIONSHIP INSERT ---
        existing_relates = set()
        with arcpy.da.SearchCursor(rel_class, keys) as search_cursor:
            for row in search_cursor:
                if row[1] == woh_globalid:
                    existing_relates.add(row[0])  # Store OIDs already related to the WOH

        with arcpy.da.SearchCursor(service_layer, ["GlobalID", "OID@"]) as sc:
            for row in sc:
                feature_guid = row[0]
                oid = row[1]
                if oid not in selected_ids:
                    continue
                if feature_guid in existing_relates:
                    arcpy.AddMessage("Feature GUID {} already related to WOH. Skipping.".format(feature_guid))
                    continue

                # insert new relationship
                with arcpy.da.InsertCursor(rel_class, keys) as cursor:
                    try:
                        cursor.insertRow((woh_globalid,feature_guid))
                        arcpy.AddMessage("Related WOH {} to {}".format(woh_globalid, feature_guid))
                    except Exception as e:
                        arcpy.AddMessage("Insert Failed: {}".format(e))
                        raise





    elif action_type == "Remove relationships":
        # --- RELATIONSHIP REMOVAL ---
        with arcpy.da.SearchCursor(service_layer, ["GlobalID"], "OBJECTID IN ({})".format(",".join(map(str, selected_ids)))) as sc_cursor:
            target_ids = [row[0] for row in sc_cursor]
            arcpy.AddMessage("{}".format(target_ids))

        with arcpy.da.UpdateCursor(rel_class, keys) as rel_cursor:
            for row in rel_cursor:
                if row[1] in target_ids and row[0] == woh_globalid:
                    rel_cursor.deleteRow()
                    arcpy.AddMessage("Removed relationship for FeatureGUID: {}".format(row[1]))

    edit.stopOperation()
    # edit.stopEditing(True)  # Save edits


for layer in service_layers:
    modify_relationships(layer)