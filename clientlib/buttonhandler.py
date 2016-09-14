import configparser, os, sys
import fliclib

def on_connection_status_changed(channel, connection_status, disconnect_reason):
    print(channel.bd_addr + " " + str(connection_status) + (" " + str(disconnect_reason) if connection_status == fliclib.ConnectionStatus.Disconnected else ""))
    
def on_button_single_or_double_click_or_hold(channel, click_type, was_queued, time_diff):
    # Execute the appropriate click function with the button address as the argument
    if not was_queued:
        click_functions[str(click_type)](channel.bd_addr)
        
def on_single_click(button_addr):
    print("on single click " + button_addr)
    pass
    
def on_double_click(button_addr):
    print("on double click " + button_addr)
    pass
    
def on_hold(button_addr):
    print("on hold " + button_addr)
    pass        
        
click_functions = {
    'ClickType.ButtonSingleClick': on_single_click,
    'ClickType.ButtonDoubleClick': on_double_click,
    'ClickType.ButtonHold': on_hold
}

class ConfigButtonHandler():
    def __init__(self):
        self.client = fliclib.FlicClient("localhost")
        
    def on_button_single_or_double_click_or_hold(self, channel, click_type, was_queued, time_diff):
        # Don't care about queued presses
        if not was_queued:
            print("Button pressed: " + channel.bd_addr)
        
    def got_button(self, bd_addr):
        cc = fliclib.ButtonConnectionChannel(bd_addr)
        cc.on_button_single_or_double_click_or_hold = self.on_button_single_or_double_click_or_hold
        self.client.add_connection_channel(cc)
        
    def got_info(self, items):
        for bd_addr in items["bd_addr_of_verified_buttons"]:
            self.got_button(bd_addr)
        
    def start(self):            
        # Get button information
        self.client.get_info(self.got_info)
        self.client.on_new_verified_button = self.got_button
        
        # Handle button events
        print("\n**********   Running in config mode   **********")
        print("Client is now listening for button events. Press a Flic button to display its address")
        self.client.handle_events()
        
        
class ButtonHandler():
    def __init__(self, lightData):
        self.client = fliclib.FlicClient("localhost")
        self.data = lightData
        
    def got_button(self, bd_addr):
        cc = fliclib.ButtonConnectionChannel(bd_addr)
        cc.on_connection_status_changed = on_connection_status_changed
        cc.on_button_single_or_double_click_or_hold = on_button_single_or_double_click_or_hold
        self.client.add_connection_channel(cc)
        
    def got_info(self, items):
        for bd_addr in items["bd_addr_of_verified_buttons"]:
            self.got_button(bd_addr)
    
    def load_config(self):
        config = configparser.ConfigParser()
        if os.path.exists("button_actions.cfg"):
            configuration = config.read_file(open("button_actions.cfg"))
            print("Found existing config file")
            self.configured = True
        else:
            print("No existing config found for button actions")
            print("Please run  in config mode to view light data and create a config file")
            sys.exit()
        
    def start(self):
        self.load_config()
            
        # Get button information
        self.client.get_info(self.got_info)
        self.client.on_new_verified_button = self.got_button
        
        # Handle button events
        print("\nClient is now listening for button events. Press a Flic button to test it out!")
        self.client.handle_events()

    
# button_actions is a dictionary that maps button ids to light actions
# e.g.
# button_actions =
# {
#       button_id_1: ToggleLight,
#       button_id_2: EnableScene
# }


    