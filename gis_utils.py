import arcpy
import os


#get the foreign and destination keys
def get_rc_keys(input_rc_table):
    """ Retrieves the origin and destination keys for a relationship class."""
    rc_desc = arcpy.Describe(input_rc_table)

    #get the origin foreign key
    origin_foreign_key = None
    for key in rc_desc.originClassKeys:
        if key[1] == "OriginForeign":
            origin_foreign_key = key[0]

    #get the destination foreign key
    dest_foreign_key = None
    for key in rc_desc.destinationClassKeys:
        if key[1] == "DestinationForeign":
            dest_foreign_key = key[0]
    return [origin_foreign_key,dest_foreign_key]

def get_sde_path(layer):
    """ Retrieves the Root SDE Path for a feature class."""

    #Find path
    layer_desc = arcpy.Describe(layer)
    layer_path = layer_desc.path
    # layer_cat_path = layer_desc.catalogPath
    root_sde = os.path.dirname(layer_path)
    # arcpy.AddMessage("Catalog Path: {}".format(layer_cat_path))
    # arcpy.AddMessage("Root SDE: {}".format(root_sde))

    #Get root SDE
    sde_path = r"{}".format(root_sde)
    return sde_path

def find_rel(fc,keyword):
    """Dynamically find a relationship class based on a keyword for a feature class.
    Returns the catalog path to the RC, or None if not found."""

    arcpy.AddMessage("Finding Relationship...")
    rel_classes = arcpy.Describe(fc).relationshipClassNames
    # arcpy.AddMessage(rel_classes)

    sde = get_sde_path(fc)
    target_rel = None
    for rel in rel_classes:
        if keyword in rel:   # adjust name filter to match your env
            rel_desc = arcpy.Describe(rel)
            target_rel = rel_desc.catalogPath
            arcpy.AddMessage("Relationship Found: {}".format(target_rel))
            break
    if not target_rel:
        arcpy.AddMessage("No relationship found for keyword: {}. Skipping..".format(keyword))


    return target_rel


def retrieve_true_name(service_layer):
    """Returns the feature class name without schema/owner prefixes."""

    desc = arcpy.Describe(service_layer)
    layer_fc = desc.featureClass.catalogPath
    layer_name = desc.featureClass.name  # e.g. "YOURSDE.Meters"

    # Split on "." and grab the last part
    true_name = layer_name.split(".")[-1]

    arcpy.AddMessage("FC Name: {}".format(true_name))
    arcpy.AddMessage("FC Path: {}".format(layer_fc))
    return true_name
