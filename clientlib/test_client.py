#!/usr/bin/env python3

# Test Client application.
#
# This program attempts to connect to all previously verified Flic buttons by this server.
# Once connected, it prints Down and Up when a button is pressed or released.
# It also monitors when new buttons are verified and connects to them as well. For example, run this program and at the same time the new_scan_wizard.py program.

import lightservice
import buttonhandler
import sys
import argparse

def main():
    # Parse arguments for configuration and light type
    parser = argparse.ArgumentParser()
    parser.add_argument("lightType", help="lifx or hue", choices=['lifx', 'hue'], type = str.lower)
    parser.add_argument("-c", "--configMode", action='store_true', help="runs the client in config mode which prints out the light data")
    
    args = parser.parse_args()
        
    configMode = args.configMode
    lightType = args.lightType
    
    # Get light information 
    # *Note*
    # Only LIFX is supported at this point in time
    light_service = None
    if lightType == 'lifx':
        light_service = lightservice.LIFXLightService("https://api.lifx.com/v1/")
    
    data = light_service.refresh_light_data(configMode)
    
    # Start up the button listener only 
    # if we aren't in config mode
    if configMode:
        sys.exit()
    else:
        button_handler = buttonhandler.ButtonHandler(data)
        button_handler.start()

if __name__ == "__main__":
    main()
