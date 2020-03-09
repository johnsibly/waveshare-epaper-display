import json
import requests
from operator import attrgetter
import os

MONZO_ACCESS_TOKEN=os.getenv("MONZO_ACCESS_TOKEN","")
MONZO_ACCOUNT_ID=os.getenv("MONZO_ACCOUNT_ID","")
MONZO_ACCOUNT_NAME=os.getenv("MONZO_ACCOUNT_NAME","")
MONZO_POT_1_NAME=os.getenv("MONZO_POT_1_NAME","")
MONZO_POT_2_NAME=os.getenv("MONZO_POT_2_NAME","")
MONZO_POT_3_NAME=os.getenv("MONZO_POT_3_NAME","")

http --form PUT "https://api.monzo.com/pots/$pot_id/deposit" \
    "Authorization: Bearer $access_token" \
    "source_account_id=$account_id" \
    "amount=$amount" \
    "dedupe_id=$dedupe_id"

{
    "id": "pot_00009exampleP0tOxWb",
    "name": "Wedding Fund",
    "style": "beach_ball",
    "balance": 550100,
    "currency": "GBP",
    "created": "2017-11-09T12:30:53.695Z",
    "updated": "2018-02-26T07:12:04.925Z",
    "deleted": false
}

monzoPotsURL = 'https://api.monzo.com/pots'

potUrl1 = ''
potUrl2 = ''
potUrl3 = ''   

headers = {'Authorization': 'Bearer ' + MONZO_ACCESS_TOKEN}
balanceJson = requests.get(monzoBalanceURL, headers=headers).json()
monzoBalance = MONZO_ACCOUNT_NAME + ': £' + "{:.2f}".format(balanceJson['balance']/100)
potsJson = requests.get(monzoPotsURL, headers=headers).json()

for pot in potsJson['pots']:
    if pot['name'] == MONZO_POT_1_NAME:
        potUrl1 = "https://api.monzo.com/pots/"+pot['id']"/deposit"
    if pot['name'] == MONZO_POT_2_NAME:
        potUrl2 = "https://api.monzo.com/pots/"+pot['id']"/deposit"
    if pot['name'] == MONZO_POT_3_NAME:
        potUrl3 = "https://api.monzo.com/pots/"+pot['id']"/deposit"

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('MONZO_BALANCE', monzoBalance)
output = output.replace('MONZO_POT_1', pot1)
output = output.replace('MONZO_POT_2', pot2)
output = output.replace('MONZO_POT_3', pot3)
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)