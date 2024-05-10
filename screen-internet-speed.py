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

if os.path.isfile("internet_speed.pickle"):
    print("Found internet_speed")
    file = open('internet_speed.pickle', 'rb')
    data = pickle.load(file)
    stale=time.time() - os.path.getmtime(os.getcwd() + "/internet_speed.pickle") > (24*60*60)
    downloadSpeed = data[1]
    uploadSpeed = data[0]
    print('Showing the pickled data: uploadSpeed = ' + uploadSpeed + ' downloadSpeed = ' + downloadSpeed)
    file.close()
if stale:
    print("Pickle is stale, working out connection speed from router")
    routerStatusUrl = 'http://192.168.10.1/sky_router_status.html'
    routerStatsUrl = 'http://192.168.10.1/sky_system.html'
    html = requests.get(routerStatusUrl, auth=HTTPBasicAuth('admin', skyrouter_password)).text

    print(html)

    upstreamFindString = 'Line Rate - Upstream (Kbps):</span><span id="router-status-linerate-up-value">\');\n'
    downstreamFindString = 'Line Rate - Downstream (Kbps):</span><span id="router-status-linerate-down-value">\');\n'
    start = html.find(upstreamFindString)
    print(start)
    uploadSpeed = html[start+len(upstreamFindString)+52:start+len(upstreamFindString)+57] # adjust end index
    start = html.find(downstreamFindString, start)
    print(start)

    downloadSpeed = html[start+len(downstreamFindString)+52:start+len(downstreamFindString)+57]
    print('uploadSpeed = ' + uploadSpeed + ' downloadSpeed = ' + downloadSpeed)

    if uploadSpeed.isnumeric() and downloadSpeed.isnumeric():
        os.remove("internet_speed.pickle")
        data = [uploadSpeed, downloadSpeed]
        file = open('internet_speed.pickle', 'wb')
        pickle.dump(data, file)
        file.close()

speed = 'Up ' + str(round(int(uploadSpeed)/1000, 1)) + ' Mbps' + ' ⚡Down ' + str(round(int(downloadSpeed)/1000, 1)) + ' Mbps'
print(speed)
# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('CONNECTION_SPEED', speed)
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
