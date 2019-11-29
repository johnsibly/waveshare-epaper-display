import json
import requests
from operator import attrgetter
import codecs

template = 'screen-output-weather.svg'

busUrl = 'https://api.tfl.gov.uk/Journey/JourneyResults/sw152qa/to/W67AP?nationalSearch=false&Mode=bus&timeIs=Departing&journeyPreference=LeastTime'
tubeUrl = 'https://api.tfl.gov.uk/Journey/JourneyResults/sw152qa/to/W67AP?nationalSearch=false&Mode=tube&timeIs=Departing&journeyPreference=LeastTime'
busArrivals = 'https://api.tfl.gov.uk/StopPoint/490006048W/arrivals'
tubeStatusUrl = 'https://api.tfl.gov.uk/line/mode/tube/status'

bus1 = ''
bus2 = ''
bus3 = ''
tubeTime = 'Undefined'
busTime = 'Undefined'

def wheresMyBus():
    global bus1, bus2, bus3
    json = requests.get(busArrivals).json()
    sortedBuses = sorted(json, key=lambda a: a['timeToStation']) 

    if len(sortedBuses) > 0:
        bus = sortedBuses[0]
        bus1 = bus['lineName'] + ' in ' + str(int(bus['timeToStation']/60)) + ' minutes'
        if len(sortedBuses) > 1:
            bus = sortedBuses[1]
            bus2 = bus['lineName'] + ' in ' + str(int(bus['timeToStation']/60)) + ' minutes'
            if len(sortedBuses) > 2:
                bus = sortedBuses[2]
                bus3 = bus['lineName'] + ' in ' + str(int(bus['timeToStation']/60)) + ' minutes'
    print(bus1)
    print(bus2)
    print(bus3)
    
def howIsJourney(tuneUrl, option):
    json = requests.get(tuneUrl).json()
    for journey in json['journeys']:
        mode = 'walking'
        for leg in journey['legs']:
            if leg['mode']['name'] != 'walking':
                if mode == 'walking':
                    mode = leg['mode']['name']
                # else:
                #    mode += ' and ' + leg['mode']['name']
        return (mode + ' will take ' + str(journey['duration']) + ' minutes')

def howIsDistrict():
    districtLineStatus = ''
    json = requests.get(tubeStatusUrl).json()
    for line in json:
        if line['name'] == 'District':
            districtLineStatus = line['lineStatuses'][0]['statusSeverityDescription']
            break
    print('District line status = ' + districtLineStatus)

busTime = howIsJourney(busUrl, 'bus')
tubeTime = howIsJourney(tubeUrl, 'tube')
wheresMyBus()

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('OPTION_TUBE', tubeTime.capitalize())
output = output.replace('OPTION_BUS', busTime.capitalize())
output = output.replace('BUS_1', bus1)
output = output.replace('BUS_2', bus2)
output = output.replace('BUS_3', bus3)
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)