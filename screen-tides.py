import pandas as pd
import codecs
template = 'screen-output-weather.svg'

url = r'https://thamestides.org.uk/todayp'
tables = pd.read_html(url) # Returns list of all tables on page
tide_table = tables[0] # Select table of interest

today = tide_table.iloc[1][1]
tomorrow = tide_table.iloc[1][4]

todayHighTime1 = tide_table.iloc[4][1]
todayHighTime2 = tide_table.iloc[6][1]
todayHighHeight1 = tide_table.iloc[4][3]
todayHighHeight2 = tide_table.iloc[6][3]

tomorrowHighTime1 = tide_table.iloc[4][4]
tomorrowHighTime2 = tide_table.iloc[6][4]
tomorrowHighHeight1 = tide_table.iloc[4][6]
tomorrowHighHeight2 = tide_table.iloc[6][6]

print('today', today)
print('tomorrow', tomorrow)
print('todayHighTime1', todayHighTime1)
print('todayHighTime2', todayHighTime2)
print('todayHighHeight1', todayHighHeight1)
print('todayHighHeight2', todayHighHeight2)
print('tomorrowHighTime1', tomorrowHighTime1)
print('tomorrowHighTime2', tomorrowHighTime2)
print('tomorrowHighHeight1', tomorrowHighHeight1)
print('tomorrowHighHeight2', tomorrowHighHeight2)

# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('todayDate', today)
output = output.replace('tomorrowDate', tomorrow)
output = output.replace('todayHighTime1', todayHighTime1)
output = output.replace('todayHighTime2', todayHighTime2)
output = output.replace('todayHighHeight1', todayHighHeight1)
output = output.replace('todayHighHeight2', todayHighHeight2)
output = output.replace('tomorrowHighTime1', tomorrowHighTime1)
output = output.replace('tomorrowHighTime2', tomorrowHighTime2)
output = output.replace('tomorrowHighHeight1', tomorrowHighHeight1)
output = output.replace('tomorrowHighHeight2', tomorrowHighHeight2)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)
