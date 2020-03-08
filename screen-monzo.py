import json
import requests
from operator import attrgetter
import codecs
import os

template = 'screen-output-weather.svg'

MONZO_ACCESS_TOKEN=os.getenv("MONZO_ACCESS_TOKEN","")
MONZO_ACCOUNT_ID=os.getenv("MONZO_ACCOUNT_ID","")
MONZO_ACCOUNT_NAME=os.getenv("MONZO_ACCOUNT_NAME","")
MONZO_POT_1_NAME=os.getenv("MONZO_POT_1_NAME","")
MONZO_POT_2_NAME=os.getenv("MONZO_POT_2_NAME","")
MONZO_POT_3_NAME=os.getenv("MONZO_POT_3_NAME","")

monzoBalanceURL = 'https://api.monzo.com/balance?' + 'account_id=' + MONZO_ACCOUNT_ID
monzoPotsURL = 'https://api.monzo.com/pots'
monzoBalance = 'Undefined'
pot1 = 'Undefined'
pot2 = 'Undefined'
pot3 = 'Undefined'   

headers = {'Authorization': 'Bearer ' + MONZO_ACCESS_TOKEN}
balanceJson = requests.get(monzoBalanceURL, headers=headers).json()
monzoBalance = MONZO_ACCOUNT_NAME + ': £' + "{:.2f}".format(balanceJson['balance']/100)
potsJson = requests.get(monzoPotsURL, headers=headers).json()

for pot in potsJson['pots']:
    if pot['name'] == MONZO_POT_1_NAME:
        pot1 = pot['name'] + ': £' + "{:.2f}".format(pot['balance']/100)
    if pot['name'] == MONZO_POT_2_NAME:
        pot2 = pot['name'] + ': £' + "{:.2f}".format(pot['balance']/100)
    if pot['name'] == MONZO_POT_3_NAME:
        pot3 = pot['name'] + ': £' + "{:.2f}".format(pot['balance']/100)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('MONZO_BALANCE', monzoBalance)
output = output.replace('MONZO_POT_1', pot1)
output = output.replace('MONZO_POT_2', pot2)
output = output.replace('MONZO_POT_3', pot3)
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)