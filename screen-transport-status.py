import json
import requests
from operator import attrgetter
import codecs

template = 'screen-output-weather.svg'

# busUrl = 'https://api.tfl.gov.uk/Journey/JourneyResults/sw152qa/to/W67AP?nationalSearch=false&Mode=bus&timeIs=Departing&journeyPreference=LeastTime'
tubeUrl = 'https://api.tfl.gov.uk/Journey/JourneyResults/sw152qa/to/NW15DH?nationalSearch=false&Mode=tube&timeIs=Departing&journeyPreference=LeastTime'
tubeStatusUrl = 'https://api.tfl.gov.uk/line/mode/tube/status'

tubeTime = 'Undefined'
busTime = 'Undefined'
    
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

# busTime = howIsJourney(busUrl, 'bus')
tubeTime = howIsJourney(tubeUrl, 'tube')

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('OPTION_TUBE', tubeTime.capitalize())
output = output.replace('OPTION_BUS', busTime.capitalize())
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)