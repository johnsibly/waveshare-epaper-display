import json
import requests
from operator import attrgetter
import codecs
from requests.auth import HTTPBasicAuth
import os
skyrouter_password=os.getenv("SKYROUTER_PASSWORD","")

template = 'screen-output-weather.svg'

downloadSpeed = 'Undefined'
uploadSpeed = 'Undefined'
    
routerStatusUrl = 'http://192.168.10.1/sky_router_status.html'
routerStatsUrl = 'http://192.168.10.1/sky_system.html'

html = requests.get(routerStatusUrl, auth=HTTPBasicAuth('admin', skyrouter_password)).text
print(html)
start = html.find('Aggregate Line Rate - Upstream (Kbps):')
print(start)
uploadSpeed = html[start:start+30] # adjust end index
print(uploadSpeed)
start = html.find('Aggregate Line Rate - Downstream (Kbps):', start)
print(start)
downloadSpeed = html[start:start+30]
print(downloadSpeed)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('OPTION_UPLOAD', 'Upload speed ' + round(uploadSpeed/1024, 1) + ' Mbps')
output = output.replace('OPTION_DOWNLOAD', 'Download speed ' + round(downloadSpeed/1024, 1) + ' Mbps')
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)