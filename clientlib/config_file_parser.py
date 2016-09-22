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
        self.action_type = None
        self.selector = None
        self.duration = None
        self.state = None
        self.states = None
        self.uuid = None

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
        self.power = None
        self.color = None
        self.duration = None
        self.brightness = None
        self.selector = None
        

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
            
    def _get_action_info(self, action, section):
        """Function to populate an action object from the config file section
        """
        action_dict = self.config[section]
        for key in action_dict:
            cameled_key = key.title().replace(" ", "")
            if cameled_key in ActionType.__members__:
                action.action_type = cameled_key
                if cameled_key == 'SetState':
                    # Store state in action object
                    action.state = self.config[section][key]
                elif cameled_key == 'SetStates':
                    # Store states in list in action object
                    action.states = [x.strip() for x in self.config[section][key].split(',')]
                elif (cameled_key == 'Toggle') \
                  or (cameled_key == 'Breathe') \
                  or (cameled_key == 'Pulse') \
                  or (cameled_key == 'Cycle'):
                    action.selector = self.config[section][key]
                elif (cameled_key == 'ActivateScene'):
                    action.uuid = self.config[section][key]
            elif cameled_key == 'Selector':
                    action.selector = self.config[section][key]
            elif cameled_key == 'Duration':
                # Store duration in action object
                action.duration = self.config[section][key]
            elif cameled_key == 'Default':
                action.default = self.config[section][key]
                
        return action         
        
    def _get_button_info(self, button, section):
        """Function to populate a button object from the config file section
        """
        for key in self.config[section]:
            if key == 'singleclick':
                button.single_click_action = self.config[section][key]
            elif key == 'doubleclick':
                button.double_click_action = self.config[section][key]  
            elif key == 'hold':
                button.hold_action = self.config[section][key]
        return button
        
    def _get_state_info(self, state, section):
        """Function to populate a state object from the config file section
        """
        for key in self.config[section]:
            if key == 'power':
                state.power = self.config[section][key]
            elif key == 'color':
                state.color = self.config[section][key]
            elif key == 'brightness':
                state.brightness = self.config[section][key]   
            elif key == 'duration':
                state.duration = self.config[section][key]
            elif key == 'selector':
                state.selector = self.config[section][key]
        return state       
        
    def get_config(self):
        """Function to get the configuration from the config file.
        
        Returns:
            A dictionary of actions, buttons and states.
            e.g.
            { 
                'actions': {ActionData},
                'buttons': {ButtonData},
                'states' : {StateData}
            }
        """
        
        actions = {}
        buttons = {}
        states = {}
        
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
                        action = self._get_action_info(action, section)
                        actions[action.action_name] = action
                        
                    elif section_type == "BUTTON":
                        button_address = self._get_section_name(section, section_type)
                        button = Button(button_address)
                        button = self._get_button_info(button, section)
                        buttons[button.button_address] = button
                        
                    elif section_type == "STATE":
                        state_name = self._get_section_name(section, section_type)
                        state = State(state_name)
                        state = self._get_state_info(state, section)
                        states[state.state_name] = state
                        
                    else:
                        print("%s not a valid section type, skipping." % section_type)
                        continue
            return { 'actions': actions, 'buttons': buttons, 'states': states}
            
        else:
            print("No existing config found for button actions")
            print("Please run  in config mode to view light data and create a config file")
            sys.exit()