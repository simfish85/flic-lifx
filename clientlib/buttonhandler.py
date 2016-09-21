import sys
import fliclib
import config_file_parser
from enum import Enum

class ConfigButtonHandler(object):
    """Listens for button clicks and prints out the button address whenever a button is clicked. This is to facilitate writing a config file to map button presses to light actions.
    """
    
    def __init__(self):
        """Inits ConfigButtonHandler by starting up a FlicClient to listen for button presses.
        """
        self.client = fliclib.FlicClient("localhost")
        
    def on_button_single_or_double_click_or_hold(self, channel, click_type, was_queued, time_diff):
        """Function to execute whenever a connected button is pressed. Prints out the button address.
    
        Args:
            channel: the button channel the click event occurred on.
            click_type: the click type that occurred.
            was_queued: bool indicating whether this was a queued click event.
            time_diff: ???
        """
        # Don't care about queued presses
        if not was_queued:
            print("Button pressed: " + channel.bd_addr)
        
    def got_button(self, bd_addr):
        """Creates a button connection channel and assigns the handler function for button presses for a particular button.
    
        Args:
            bd_addr: button address.
        """
        cc = fliclib.ButtonConnectionChannel(bd_addr)
        cc.on_button_single_or_double_click_or_hold = self.on_button_single_or_double_click_or_hold
        self.client.add_connection_channel(cc)
        
    def got_info(self, items):
        """Handler for getting info from the button server. Calls got_button for each button address it receives from the server.
    
        Args:
            items: information retrieved from the server. We only care about the button addresses of verified buttons.
        """
        for bd_addr in items["bd_addr_of_verified_buttons"]:
            self.got_button(bd_addr)
        
    def start(self):     
        """Initializes the ButtonConnectionChannels and starts listening for button events.
        """       
        # Get button information
        self.client.get_info(self.got_info)
        self.client.on_new_verified_button = self.got_button
        
        # Handle button events
        print("\n**********   Running in config mode   **********")
        print("Client is now listening for button events. Press a Flic button to display its address")
        self.client.handle_events()
        
        
class ButtonHandler(object):
    """Handles button presses by calling the appropriate function for the button action that occurred.
    """
    
    class SectionType(Enum):
        Action = 'ACTION'
        Button = 'BUTTON'
        State = 'STATE'
    
    def __init__(self, light_data):
        """Inits ButtonHandler by starting up a FlicClient to listen for button presses. Also creates a dictionary mapping click types to functions to handle them.
        
        Args:
            light_data: light information retrieved from the lightservice.
        """
        self.client = fliclib.FlicClient("localhost")
        self.data = light_data
        self.click_functions = {
            'ClickType.ButtonSingleClick': self.on_single_click,
            'ClickType.ButtonDoubleClick': self.on_double_click,
            'ClickType.ButtonHold': self.on_hold
        }
        self.buttons_actions = {}
    
    def on_connection_status_changed(self, channel, connection_status, disconnect_reason):
        """Function that is called whenever a buttons connection status is changed.
        
        Args:
            channel: button channel that had a connection status change.
            connection_status: the current connection_status.
            disconnect_reason: the reason why the connection was disconnected (if it was disconnected).
        """
        pass
        
    def on_button_single_or_double_click_or_hold(self, channel, click_type, was_queued, time_diff):
        """Function to execute whenever a connected button is pressed. Executes the appropriate click_type handler function.
    
        Args:
            channel: the button channel the click event occurred on.
            click_type: the click type that occurred.
            was_queued: bool indicating whether this was a queued click event.
            time_diff: ???
        """
        # Execute the appropriate click function with the button address as the argument
        if not was_queued:
            self.click_functions[str(click_type)](channel.bd_addr)
            
    def on_single_click(self, button_addr):
        """Function to handle single clicks for a certain button.
        
        Args:
            button_addr: address of the button that was clicked.
        """
        print("on single click " + button_addr)
        
    def on_double_click(self, button_addr):
        """Function to handle double clicks for a certain button.
        
        Args:
            button_addr: address of the button that was clicked.
        """
        print("on double click " + button_addr)
        
    def on_hold(self, button_addr):
        """Function to handle a button hold for a certain button.
        
        Args:
            button_addr: address of the button that was clicked.
        """
        print("on hold " + button_addr)
            
    def got_button(self, bd_addr):
        """Creates a button connection channel and assigns the handler function for button presses for a particular button.
    
        Args:
            bd_addr: button address.
        """
        cc = fliclib.ButtonConnectionChannel(bd_addr)
        cc.on_connection_status_changed = self.on_connection_status_changed
        cc.on_button_single_or_double_click_or_hold = self.on_button_single_or_double_click_or_hold
        self.client.add_connection_channel(cc)
        
    def got_info(self, items):
        """Handler for getting info from the button server. Calls got_button for each button address it receives from the server.
    
        Args:
            items: information retrieved from the server. We only care about the button addresses of verified buttons.
        """
        for bd_addr in items["bd_addr_of_verified_buttons"]:
            self.got_button(bd_addr)
    
    def load_config(self):
        """Loads the button config from the config file. Essentially maps button click types to light actions.
        """
        config = config_file_parser.ConfigFileParser()
        config_data = config.get_config()
        print(config_data)
        
    def start(self):
        """Loads the button config, initializes the ButtonConnectionChannels, and starts listening for button events.
        """
        self.load_config()
            
        # Get button information
        self.client.get_info(self.got_info)
        self.client.on_new_verified_button = self.got_button
        
        # Handle button events
        print("\nClient is now listening for button events. Press a Flic button to test it out!")
        self.client.handle_events()


    