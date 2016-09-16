import configparser
import os
import re

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
        
    def _get_section_type(self, section):
        section_type_regex = re.compile("^[A-Z]+\\b")
        match = section_type_regex.match(section)
        if match is None or match.group() not in ConfigFileParser.valid_section_names:
            print("%s not a valid section name, skipping." % section)
        else:
            print("Found section with type: %s" % match.group())
        
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
            
        else:
            print("No existing config found for button actions")
            print("Please run  in config mode to view light data and create a config file")
            sys.exit()