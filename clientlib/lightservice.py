import requests
import os
import json

token = os.environ['TOKEN']
headers = {
    "Authorization": "Bearer %s" % token,
}

class LightDataService():
    def __init__(self):
        pass
        
    def refresh_light_data(self):
        response = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
        light_data = json.loads(response.text)
        print(light_data)