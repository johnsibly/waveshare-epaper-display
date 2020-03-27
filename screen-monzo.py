import json
import requests
from operator import attrgetter
import codecs
import os
from pymonzo import MonzoAPI
monzo = MonzoAPI() 

template = 'screen-output-weather.svg'

MONZO_ACCOUNT_NAME=os.getenv("MONZO_ACCOUNT_NAME","")
MONZO_POT_1_NAME=os.getenv("MONZO_POT_1_NAME","")
MONZO_POT_2_NAME=os.getenv("MONZO_POT_2_NAME","")
MONZO_POT_3_NAME=os.getenv("MONZO_POT_3_NAME","")

monzoBalance = 'Undefined'
pot1 = 'Undefined'
pot2 = 'Undefined'
pot3 = 'Undefined'   

monzoBalance = MONZO_ACCOUNT_NAME + ': £' + "{:.2f}".format(monzo.balance().balance/100)

pots = monzo.pots()
for pot in pots:
    if pot.name == MONZO_POT_1_NAME:
        pot1 = str(pot.name) + ': £' + "{:.2f}".format(float(pot.balance)/100)
    if pot.name == MONZO_POT_2_NAME:
        pot2 = str(pot.name) + ': £' + "{:.2f}".format(float(pot.balance)/100)
    if pot.name == MONZO_POT_3_NAME:
        pot3 = str(pot.name) + ': £' + "{:.2f}".format(float(pot.balance)/100)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('MONZO_BALANCE', monzoBalance)
output = output.replace('MONZO_POT_1', pot1)
output = output.replace('MONZO_POT_2', pot2)
output = output.replace('MONZO_POT_3', pot3)
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
