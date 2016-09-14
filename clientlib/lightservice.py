import requests
import os
import json
import stringformatter

token = os.environ['TOKEN']
headers = {
    "Authorization": "Bearer %s" % token,
}
all_lights_suffix = "lights/all"
scenes_suffix = "scenes"

class LIFXGroup():
    def __init__(self, groupId, groupName):
        self.groupId = groupId
        self.groupName = groupName
        self.lights = list()
        
    def add_light(self, light):
        self.lights.append(light)

    def __repr__(self):
        return """
        LIFX Group:
        Group ID: %s
        Group Name: %s
        Lights:\n""" % (self.groupId, self.groupName) + stringformatter.lights_to_string(self.lights, False)
        
class LIFXLocation():
    def __init__(self, locationId, locationName):
        self.locationId = locationId
        self.locationName = locationName
        self.lights = list()
        
    def add_light(self, light):
        self.lights.append(light)    

    def __repr__(self):
        return """
        LIFX Location: 
        Location ID: %s
        Location Name: %s
        Lights:\n""" % (self.locationId, self.locationName) + stringformatter.lights_to_string(self.lights, False)

class LIFXLightService():
    # Params:
    # endpoint_base_url: Base url for LIFX Api
    def __init__(self, endpoint_base_url):
        self.endpoint_base_url = endpoint_base_url
        
    # Returns a dictionary of Lights, Groups, Locations, and Scenes
    # e.g.
    # {
    #    'lights': {LightData}, 
    #    'groups': {GroupData},
    #    'locations': {LocationData},
    #    'scenes': {SceneData}
    # }
    def refresh_light_data(self, isConfigMode):
        light_info = self.get_light_data()
        lights = light_info['lights']
        groups = light_info['groups']
        locations = light_info['locations']
        scenes = self.get_scene_data()
        
        if isConfigMode:
            print(stringformatter.lights_to_string(lights, True))
            print(stringformatter.dict_to_string(groups, "GROUPS"))
            print(stringformatter.dict_to_string(locations, "LOCATIONS"))
            print(stringformatter.scenes_to_string(scenes))
        
        return  { 
                    'lights': lights,
                    'groups': groups,
                    'locations': locations,
                    'scenes': scenes
                }
        
    # Returns a dictionary of Lights, Groups, and Locations
    # e.g.
    # {
    #    'lights': {LightData},
    #    'groups': {GroupData},
    #    'locations': {Locations}
    # }
    # Lifx api doesn't give an easy way to get group
    # information like it does for scenes so we need
    # to get group information from light information
    def get_light_data(self):
        response = requests.get(self.endpoint_base_url + all_lights_suffix, headers=headers)
        lights = json.loads(response.text)
        
        # Init the groups and locations dictionaries
        groups = {}
        locations = {}
        for light in lights:
            
            # Get group information
            group_info = light["group"]
            group_id = group_info["id"]
            group_name = group_info["name"]
            
            # If group exists already, add the light to it
            if group_id in groups:
                groups[group_id].add_light(light)
            # Else if the group doesn't exist yet, create it and add the light to it
            else:
                groups[group_id] = LIFXGroup(group_id, group_name)
                groups[group_id].add_light(light)
                
                
            # Get location information
            location_info = light["location"]
            location_id = location_info["id"]
            location_name = location_info["name"]
                
            # If location exists already, add the light to it
            if location_id in locations:
                locations[location_id].add_light(light)
            # Else if the location doesn't exist yet, create it and add the light to it
            else:
                locations[location_id] = LIFXLocation(location_id, location_name)
                locations[location_id].add_light(light)
            
        return { 'lights': lights, 'groups': groups, 'locations': locations }
            
    # Returns a list of Scenes
    def get_scene_data(self):
        response = requests.get(self.endpoint_base_url + scenes_suffix, headers=headers)
        scenes = json.loads(response.text)
        return scenes