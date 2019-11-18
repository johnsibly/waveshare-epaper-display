from __future__ import print_function
import datetime
import time
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import codecs
import os

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
template = 'screen-output-weather.svg'

google_calendar_id=os.getenv("GOOGLE_CALENDAR_ID","primary")

creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)


events_result = None
stale = True

if(os.path.isfile(os.getcwd() + "/calendar.pickle")):
    print("Found cached calendar response")
    with open('calendar.pickle','rb') as cal:
        events_result = pickle.load(cal)
    stale=time.time() - os.path.getmtime(os.getcwd() + "/calendar.pickle") > (1*60*60)

if stale:
    print("Pickle is stale, calling the Calendar API")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId=google_calendar_id, timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    with open('calendar.pickle', 'wb') as cal:
        pickle.dump(events_result, cal)

events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')

output = codecs.open(template , 'r', encoding='utf-8').read()
for x in range(6):
    if events[x]:
        event = events[x]
        start = event['start'].get('dateTime', event['start'].get('date'))
        day = ''
        if len(start) == 10:
            day = time.strftime("%a %b %d",time.strptime(start,"%Y-%m-%d"))
        else:
            day = time.strftime("%a %b %d %X",time.strptime(start,"%Y-%m-%dT%H:%M:%S%fZ"))
        desc = event['summary']
        print(day, desc)
    else:
        day = ''
        desc = ''
    DAY_TOKEN = 'CAL_' + str(x+1)
    DESC_TOKEN = 'CAL_DESC_' + str(x+1)
    output = output.replace(DAY_TOKEN, day)
    output = output.replace(DESC_TOKEN, desc)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
