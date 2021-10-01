import json
import requests
from operator import attrgetter
import codecs
from requests.auth import HTTPBasicAuth
import os
import pickle
skyrouter_password=os.getenv("SKYROUTER_PASSWORD","")


template = 'screen-output-weather.svg'

downloadSpeed = 'Undefined'
uploadSpeed = 'Undefined'

if os.path.isfile('internet_speed'):
    file = open('internet_speed', 'rb')
    data = pickle.load(file)
    file.close()
    downloadSpeed = data[1]
    uploadSpeed = data[0]
    print('Showing the pickled data: uploadSpeed = ' + uploadSpeed + ' downloadSpeed = ' + downloadSpeed)
else:
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
    file = open('internet_speed', 'wb')
    pickle.dump(data, file)
    file.close()

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('OPTION_UPLOAD', 'Upload speed ' + str(round(int(uploadSpeed)/1024, 1)) + ' Mbps')
output = output.replace('OPTION_DOWNLOAD', 'Download speed ' + str(round(int(downloadSpeed)/1024, 1)) + ' Mbps')
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)