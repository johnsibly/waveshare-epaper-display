#!/usr/bin/python

import json
import requests
from xml.dom import minidom
import datetime
import codecs
import os.path
import time
import sys
import os
import html

darksky_apikey=os.getenv("DARKSKY_APIKEY","")

if darksky_apikey=="" or darksky_apikey=="xxxxxxxxxxxxxx":
    print("DARKSKY_APIKEY is missing")
    sys.exit(1)

town_latlong='51.4616,-0.2090'

template = 'screen-template.svg'


#Map DarkSky icons to local icons
#Reference: https://openweathermap.org/weather-conditions

icon_dict={
    'clear-day':'skc',
    'clear-night':'clearnight',
    'rain':'ra',
    'snow':'sn',
    'sleet':'mix',
    'wind':'wind2',
    'fog':'fg',
    'cloudy':'ovc',
    'partly-cloudy-day':'sct',
    'partly-cloudy-night':'partlycloudynight',
    'hail':'rasn',
    'thunderstorm':'tsra',
    'tornado':'nsurtsra'
}

weather_json=''
stale=True

if(os.path.isfile(os.getcwd() + "/apiresponse.json")):
    #Read the contents anyway
    with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
        weather_json = content_file.read()
    stale=time.time() - os.path.getmtime(os.getcwd() + "/apiresponse.json") > (1*60*60)

#If old file or file doesn't exist, time to download it
if(stale):
    try:
        print("Old file, attempting re-download")
        url='https://api.darksky.net/forecast/' + darksky_apikey + '/' + town_latlong + '?units=si&exclude=minutely,hourly'
        weather_json = requests.get(url).text
        with open(os.getcwd() + "/apiresponse.json", "w") as text_file:
            text_file.write(weather_json)
    except:
        print("Failed to get new API response, will use older response")
        with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
            weather_json = content_file.read()

weatherData = json.loads(weather_json)

#icon_one = weatherData['daily']['data'][0]['icon']
icon_one = weatherData['currently']['icon']
high_one = round(weatherData['daily']['data'][0]['temperatureMax'])
low_one = round(weatherData['daily']['data'][0]['temperatureMin'])
day_one = time.strftime('%a %b %d', time.localtime(weatherData['daily']['data'][0]['time']))
latest_alert=""

if 'alerts' in weatherData:
    latest_alert = html.escape(weatherData['alerts'][0]['title'])

print(icon_one , high_one, low_one, day_one)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE',icon_dict[icon_one])
output = output.replace('HIGH_ONE',str(high_one))
output = output.replace('LOW_ONE',str(low_one)+"°C")
output = output.replace('DAY_ONE',day_one)

output = output.replace('TIME_NOW',datetime.datetime.now().strftime("%H:%M"))

output = output.replace('ALERT_MESSAGE', latest_alert)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)





