# LIFX & Flic Hub For Raspberry Pi
Tested on Raspbian for Raspberry Pi and on a laptop running Ubuntu 14.04

## Requirements
- Raspberry Pi (only tested on Raspberry Pi 3 Model B Board)
- The standard C/C++ libraries, which should be installed by default on raspbian
- Python 3+
- [Voltos](http://voltos.io) account (put voltos in your PATH to use the start script with ease)

## Running

### First time setup and run:
1. Create a [Voltos](http://voltos.io) bundle called "LIFXToken" and set it as the bundle in use  
`voltos create LIFXToken`    
`voltos use LIFXToken`  
2. Set a secret called "TOKEN" with your LIFX token from [cloud.lifx.com](https://cloud.lifx.com) as the value  
`voltos set TOKEN=<your LIFX token>`  
2. Execute `./setup.sh` and follow instructions.  
3. Execute `./start.sh`.

### Restarting the client (buttons already setup):
Execute `./start.sh`.

## Feedback
Be sure to post a Github issue if you find a bug, something you don't like or if something is wrong or should be changed. You can also submit a Pull request if you have a ready improvement.
