#!/usr/bin/env python3

# Test Client application.
#
# This program attempts to connect to all previously verified Flic buttons by this server.
# Once connected, it prints Down and Up when a button is pressed or released.
# It also monitors when new buttons are verified and connects to them as well. For example, run this program and at the same time the new_scan_wizard.py program.

import fliclib
import lightservice

client = fliclib.FlicClient("localhost")

def on_connection_status_changed(channel, connection_status, disconnect_reason):
    print(channel.bd_addr + " " + str(connection_status) + (" " + str(disconnect_reason) if connection_status == fliclib.ConnectionStatus.Disconnected else ""))
    
def on_button_up_or_down(channel, click_type, was_queued, time_diff):
    print(channel.bd_addr + " " + str(click_type))
    
def on_button_click_or_hold(channel, click_type, was_queued, time_diff):
    print(channel.bd_addr + " " + str(click_type))
    
def on_button_single_or_double_click(channel, click_type, was_queued, time_diff):
    print(channel.bd_addr + " " + str(click_type))
    
def on_button_single_or_double_click_or_hold(channel, click_type, was_queued, time_diff):
    print(channel.bd_addr + " " + str(click_type))  

def got_button(bd_addr):
    cc = fliclib.ButtonConnectionChannel(bd_addr)
    # Only allowing status changes and all click type handlers
    # Functions to print out information implemented above if we wish
    # to user at a later time.
    cc.on_connection_status_changed = on_connection_status_changed
    cc.on_button_single_or_double_click_or_hold = on_button_single_or_double_click_or_hold
    client.add_connection_channel(cc)

def got_info(items):
    for bd_addr in items["bd_addr_of_verified_buttons"]:
        got_button(bd_addr)

def main():
    # Get light information
    lifxService = lightservice.LightDataService()
    lifxService.refresh_light_data()
    
    # Setup button listener
    print("\nClient is now listening for button events. Press a Flic button to test it out!")
    client.get_info(got_info)
    client.on_new_verified_button = got_button
    client.handle_events()

if __name__ == "__main__":
    main()
