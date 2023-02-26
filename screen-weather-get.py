#!/usr/bin/python

import datetime
import codecs

from metofficedatahub import get_weather 

weatherData = get_weather()
    # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
template = 'screen-template.svg'

weatherData = get_weather()

icon_one = weatherData['icon']
high_one = round(weatherData['temperatureMax'])
low_one = round(weatherData['temperatureMin'])
day_one = datetime.datetime.now().strftime('%a %b %d')
latest_alert=""

if 'alerts' in weatherData:
    latest_alert = html.escape(weatherData['alerts'][0]['title'])

print(icon_one , high_one, low_one, day_one)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('ICON_ONE',icon_one)
output = output.replace('HIGH_ONE',str(high_one))
output = output.replace('LOW_ONE',str(low_one)+"°C")
output = output.replace('DAY_ONE',day_one)

output = output.replace('TIME_NOW',datetime.datetime.now().strftime("%H:%M"))

output = output.replace('ALERT_MESSAGE', latest_alert)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)





