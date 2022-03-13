import json
import requests
import time
from operator import attrgetter
import codecs
from requests.auth import HTTPBasicAuth
import os
import pickle
skyrouter_password=os.getenv("SKYROUTER_PASSWORD","")


template = 'screen-output-weather.svg'

downloadSpeed = 'Undefined'
uploadSpeed = 'Undefined'

stale = True

if os.path.isfile(os.getcwd() + "internet_speed.pickle"):
    print("Found internet_speed")
    file = open('internet_speed.pickle', 'rb')
    data = pickle.load(file)
    stale=time.time() - os.path.getmtime(os.getcwd() + "/internet_speed.pickle") > (24*60*60)

    file.close()
    downloadSpeed = data[1]
    uploadSpeed = data[0]
    print('Showing the pickled data: uploadSpeed = ' + uploadSpeed + ' downloadSpeed = ' + downloadSpeed)

if stale:
    print("Pickle is stale, working out connection speed from router")
    routerStatusUrl = 'http://192.168.10.1/sky_router_status.html'
    routerStatsUrl = 'http://192.168.10.1/sky_system.html'
    html = requests.get(routerStatusUrl, auth=HTTPBasicAuth('admin', skyrouter_password)).text
    
    upstreamFindString = 'Aggregate Line Rate - Upstream (Kbps):</span><span>\');\n'
    downstreamFindString = 'Aggregate Line Rate - Downstream (Kbps):</span><span>\');\n'
    start = html.find(upstreamFindString)
    print(start)
    uploadSpeed = html[start+len(upstreamFindString)+52:start+len(upstreamFindString)+57] # adjust end index
    start = html.find(downstreamFindString, start)
    print(start)

    downloadSpeed = html[start+len(downstreamFindString)+52:start+len(downstreamFindString)+57]
    print('uploadSpeed = ' + uploadSpeed + ' downloadSpeed = ' + downloadSpeed)
    
    data = [uploadSpeed, downloadSpeed]
    file = open('internet_speed.pickle', 'wb')
    
    pickle.dump(data, file)
    file.close()

speed = 'Up ' + str(round(int(uploadSpeed)/1024, 1)) + ' Mbps' + ' ⚡Down ' + str(round(int(downloadSpeed)/1024, 1)) + ' Mbps'
print(speed)
# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('CONNECTION_SPEED', speed)
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)