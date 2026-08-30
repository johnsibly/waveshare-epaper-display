#!/usr/bin/python

import datetime
import html
import codecs

from metofficedatahub import get_forecast

template = 'screen-template.svg'

# Today gets the full hero treatment; the next two days are shown as a mini strip.
forecast = get_forecast(days=3)

output = codecs.open(template , 'r', encoding='utf-8').read()

for index, label in enumerate(['ONE', 'TWO', 'THREE']):
    if index >= len(forecast):
        break
    day = forecast[index]
    icon = day['icon']
    high = round(day['temperatureMax'])
    low = round(day['temperatureMin'])
    day_name = day['date'].strftime('%a %b %d') if label == 'ONE' else day['date'].strftime('%a')

    print(label, icon, high, low, day_name)

    output = output.replace('ICON_' + label, icon)
    output = output.replace('HIGH_' + label, str(high))
    output = output.replace('LOW_' + label, str(low) + "°C")
    output = output.replace('DAY_' + label, day_name)

latest_alert = ""
if 'alerts' in forecast[0]:
    latest_alert = html.escape(forecast[0]['alerts'][0]['title'])

output = output.replace('TIME_NOW',datetime.datetime.now().strftime("%H:%M"))

output = output.replace('ALERT_MESSAGE', latest_alert)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)





