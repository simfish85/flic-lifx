#!/usr/bin/env python3

# Scan Wizard application.
#
# This program starts scanning of new Flic buttons that have not previously been verified by the server.
# Once it finds a button that is in private mode, it shows a message that the user should hold it down for 7 seconds to make it public.
# Once it finds a button that is in public mode, it attempts to connect to it.
# If it could be successfully connected and verified, the bluetooth address is printed and the user is asked if they want to scan again for another button.
# If it could not be verified within 30 seconds, the scan is restarted.

import fliclib
import sys

client = None

def strtobool(val):
    return val.lower() in ("yes", "y", "1")

def ask(question):
    while True:
        print(question, end=" [y/n] ")
        answer = input().lower()    
        try:
            bAnswer = strtobool(answer)
            return bAnswer
        except ValueError:
            print("Please respond with 'yes' or 'no'")
            
def reset_client_and_scan():
    client = fliclib.FlicClient("localhost")
    scan_for_button(client)
    
def close_client():
    print("Exiting scan wizard...")
    sys.exit()
			
def scan_for_button(client):
    wizard = fliclib.ScanWizard()
    wizard.on_found_private_button = on_found_private_button
    wizard.on_found_public_button = on_found_public_button
    wizard.on_button_connected = on_button_connected
    wizard.on_completed = on_completed
    client.add_scan_wizard(wizard)
    client.handle_events()

def on_found_private_button(scan_wizard):
    print("Found a private button. Please hold it down for 7 seconds to make it public.")

def on_found_public_button(scan_wizard, bd_addr, name):
    print("Found public button " + bd_addr + " (" + name + "), now connecting...")

def on_button_connected(scan_wizard, bd_addr, name):
    print("The button was connected, now verifying...")

def on_completed(scan_wizard, result, bd_addr, name):
    print("Scan wizard completed with result " + str(result) + ".")
    if result == fliclib.ScanWizardResult.WizardSuccess:
        print("Your button is now ready. The bd addr is " + bd_addr + ".")
        if ask("Do you want to scan for another button?"):
            print("Scanning for button... please press a Flic button to connect it.")
            reset_client_and_scan()
        else:
            close_client()
    elif result == fliclib.ScanWizardResult.WizardFailedTimeout:
        print("Timed out waiting for a Flic button, it may already be connected.")
        if ask("Do you want to try again?"):
            print("Scanning for button... please press a Flic button to connect it.")
            reset_client_and_scan()
        else:
            close_client()
    else:
        if ask("Button connection failed. Do you want to scan again?"):
            print("Scanning for button... please press a Flic button to connect it.")
            reset_client_and_scan()
        else:
            close_client()

def main():
    print("\nWelcome to Scan Wizard. Please press a Flic button to connect it.")
    reset_client_and_scan()

if __name__ == "__main__":
    main()

