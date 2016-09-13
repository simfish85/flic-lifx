# Formats strings for the command line

def lights_to_string(lights, should_print_header):
    finalString = ""
    
    if should_print_header:
        finalString += "\n-------------------------------------------"
        finalString += "\n              LIGHTS"
        finalString += "\n-------------------------------------------\n"
    
    for light in lights:
        if not should_print_header:
            finalString += "            "
        lightString = "Light ID: %s, Light Name: %s\n" % (light["id"], light["label"])
        finalString += lightString
        
    return finalString
    
def dict_to_string(values, header):
    finalString = "\n-------------------------------------------"
    finalString += "\n              " + header
    finalString += "\n-------------------------------------------\n"
    
    finalString += str(values)
        
    return finalString
    
def scenes_to_string(scenes):
    finalString = "\n-------------------------------------------"
    finalString += "\n              SCENES"
    finalString += "\n-------------------------------------------\n"
    
    for scene in scenes:
        finalString += "Scene ID: %s, Scene Name: %s\n" % (scene["uuid"], scene["name"])
        
    return finalString
    