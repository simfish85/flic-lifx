#!/usr/bin/env python3

import lightservice
import buttonhandler
import sys
import argparse

def main():
    """Main client for listening to button presses and executing the correct handlers to do light events. 
    """
    # Parse arguments for configuration and light type
    parser = argparse.ArgumentParser()
    parser.add_argument("light_type", help="lifx or hue", choices=['lifx', 'hue'], type = str.lower)
    parser.add_argument("-c", "--config_mode", action='store_true', help="runs the client in config mode which prints out the light data")
    
    args = parser.parse_args()
        
    config_mode = args.config_mode
    light_type = args.light_type
    
    # Get light information 
    # *Note*
    # Only LIFX is supported at this point in time
    light_service = None
    if light_type == 'lifx':
        light_service = lightservice.LIFXLightService("https://api.lifx.com/v1/")
    
    data = light_service.refresh_light_data(config_mode)
    
    button_handler = None
    if config_mode:
        button_handler = buttonhandler.ConfigButtonHandler()
    else:
        button_handler = buttonhandler.ButtonHandler(data)
    
    button_handler.start()

if __name__ == "__main__":
    main()
