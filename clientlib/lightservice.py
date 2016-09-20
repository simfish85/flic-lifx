import requests
import os
import json
import stringformatter
from enum import Enum

token = os.environ['TOKEN']
headers = {
    "Authorization": "Bearer %s" % token,
}    

class LIFXGroup(object):
    """Representation of a location for LIFX groups.
    """
    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name
        self.lights = list()
        
    def add_light(self, light):
        self.lights.append(light)

    def __repr__(self):
        return """
        LIFX Group:
        Group ID: %s
        Group Name: %s
        Lights:\n""" % (self.group_id, self.group_name) + stringformatter.lights_to_string(self.lights, False)
        
class LIFXLocation(object):
    """Representation of a location for LIFX lights.
    """
    
    def __init__(self, location_id, location_name):
        self.location_id = location_id
        self.location_name = location_name
        self.lights = list()
        
    def add_light(self, light):
        self.lights.append(light)    

    def __repr__(self):
        return """
        LIFX Location: 
        Location ID: %s
        Location Name: %s
        Lights:\n""" % (self.location_id, self.location_name) + stringformatter.lights_to_string(self.lights, False)

class LIFXLightService(object):
    """Service to handle all LIFX Api requests.
    
    Attributes:
        all_lights_suffix: url suffix to get all lights
        scenes_suffix: url suffix to get scenes
    """
    
    all_lights_suffix = "lights/all"
    scenes_suffix = "scenes"
    
    def __init__(self, endpoint_base_url):
        """Initializes the LIFXLightService by setting the endpoint_base_url.
        
        Args:
            endpoint_base_url: Base url for LIFX Api to base all requests off.
        """
        self.endpoint_base_url = endpoint_base_url
        
    def refresh_light_data(self, is_config_mode):
        """Gets all lights, groups, locations and scenes from the LIFX Api.
        
        Args:
            is_config_mode: if True, will print all information to console to help with writing the config file.
    
        Returns:
            A dictionary of Lights, Groups, Locations, and Scenes.
            e.g.
            {
               'lights': {LightData},
               'groups': {GroupData},
               'locations': {LocationData},
               'scenes': {SceneData}
            }
        """
        light_info = self.get_light_data()
        lights = light_info['lights']
        groups = light_info['groups']
        locations = light_info['locations']
        scenes = self.get_scene_data()
        
        if is_config_mode:
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
        
    
    def get_light_data(self):
        """Sends a request to the LIFX Api to get all light data.
    
        Returns:
            A dictionary of Lights, Groups, and Locations.
            e.g.
            {
               'lights': {LightData},
               'groups': {GroupData},
               'locations': {Locations}
            }
            Lifx api doesn't give an easy way to get group
            information like it does for scenes so we need
            to get group information from light information.
        """
        response = requests.get(self.endpoint_base_url + LIFXLightService.all_lights_suffix, headers=headers)
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
            
    def get_scene_data(self):
        """Sends a request to the LIFX Api to get all scenes.
    
        Returns:
            A list of scenes.
        """
        response = requests.get(self.endpoint_base_url + LIFXLightService.scenes_suffix, headers=headers)
        scenes = json.loads(response.text)
        return scenes
        
    def toggle(self, Selector):
        """Sends a request to the LIFX Api to toggle all matches for the selector.
        """
        # TODO
        pass
       
    def set_state(self, Selector):
        """Sends a request to the LIFX Api to set a state matching a selector.
        """
        # TODO
        pass
        
    def set_states(self, states):
        """Sends a request to the LIFX Api to set multiple states matching selectors.
        """
        # TODO
        pass