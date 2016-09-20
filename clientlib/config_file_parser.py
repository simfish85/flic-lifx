import configparser
import os
import re
from enum import Enum

class Selector(Enum):
    """Different selectors we can use for the LIFX Api.
    """
    All = "all"
    Label = "label:"
    ID = "id:"
    GroupID = "group_id:"
    Group = "group:"
    LocationID = "location_id:"
    Location = "location:"
    SceneID = "scene_id:"
    
class StateType(Enum):
    """Different states we can set via the LIFX Api.
    """
    Power = "power"
    Color = "color"
    Brightness = "brightness"
    Duration = "duration"
    
class ActionType(Enum):
    """Different action types supported.
    """
    SetState = "set_state"
    SetStates = "set_states"
    Toggle = "toggle"
    Breathe = "breathe"
    Pulse = "pulse"
    Cycle = "cycle"
    ActivateScene = "activate_scene"

class Action(object):
    """Representation of a light/button action.
    """
    
    def __init__(self, action_name):
        """Inits the action name for the Action.
        """
        self.action_name = action_name

class Button(object):
    """Representation of a button which has 3 button click types: single click, double click, and hold with actions for each event.
    """
    
    def __init__(self, button_address):
        """Sets the button address and initializes each click type to None.
        """
        self.button_address = button_address
        self.single_click_action = None
        self.double_click_action = None
        self.hold_action = None    
        
class State(object):
    """Representation of a state in the config file.
    """
    
    def __init__(self, state_name):
        """Sets the state_name for the State.
        """
        self.state_name = state_name
        

class ConfigFileParser(object):
    """Loads up the configuration from the config file.
    Attributes:
        config_file_name: name of the config file to load config settings from.
        valid_section_names: section names we process.
    """
    
    config_file_name = "button_actions.cfg"
    
    valid_section_names = ['ACTION', 'BUTTON', 'STATE']
    
    
    def __init__(self):
        """Inits ConfigFileParser by initiating a ConfigParser object.
        """
        self.config = configparser.ConfigParser()
        
    def _get_section_name(self, section, section_type):
        """Function to get the section name for a section in the config file.
        """
        section_name_regex = re.compile("^%s\s(.+)" % section_type)
        match = section_name_regex.match(section)
        if match is None:
            print("%s not a valid section header (TYPE <section name>), skipping." % section)
            return None
        else:
            return match.group(1)
        
    def _get_section_type(self, section):
        """Function to the section type for a section in the config file.
        """
        section_type_regex = re.compile("^[A-Z]+\\b")
        match = section_type_regex.match(section)
        if match is None or match.group() not in ConfigFileParser.valid_section_names:
            print("%s not a valid section type, skipping." % section)
            return None
        else:
            return match.group()
        
    def get_config(self):
        """Function to get the configuration from the config file.
        """
        
        if os.path.exists(ConfigFileParser.config_file_name):
            self.config.read_file(open(ConfigFileParser.config_file_name))
            config_sections = self.config.sections()
            
            if not len(config_sections):
                print("No sections declared in the config file...")
                print("Please add some sections to the config file before running the client.")
                sys.exit()
            else:                
                for section in config_sections:
                    section_type = self._get_section_type(section)
                    if section_type == "ACTION":
                        action_name = self._get_section_name(section, section_type)
                        action = Action(action_name)
                        print("Action name: %s" % action.action_name)
                        
                    elif section_type == "BUTTON":
                        button_address = self._get_section_name(section, section_type)
                        button = Button(button_address)
                        print("Button address: %s" % button.button_address)
                        
                    elif section_type == "STATE":
                        state_name = self._get_section_name(section, section_type)
                        state = State(state_name)
                        print("State name: %s" % state.state_name)
                        
                    else:
                        print("%s not a valid section type, skipping." % section_type)
                        continue
            
        else:
            print("No existing config found for button actions")
            print("Please run  in config mode to view light data and create a config file")
            sys.exit()