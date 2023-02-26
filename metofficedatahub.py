import logging
from datetime import datetime, timezone
from astral import LocationInfo
from astral.sun import sun
import json
import requests
import os.path
import os

location_lat = 51.4616
location_long = -0.2090

client_id=os.getenv("METOFFICEDATAHUB_CLIENT_ID","")
client_secret=os.getenv("METOFFICEDATAHUB_CLIENT_SECRET","")

if client_id=="" or client_secret=="" or client_id=="xxxxxx" or client_secret=="xxxxxx":
    print("MetOffice API credentials are missing")
    sys.exit(1)

def is_daytime(location_lat, location_long):
    """
    Return whether it's daytime for a given lat/long.
    """

    # adjust icon for sunrise and sunset
    dt = datetime.now(timezone.utc)
    city = LocationInfo(location_lat, location_long)
    s = sun(city.observer, date=dt)
    verdict = False
    if dt > s['sunset'] or dt < s['sunrise']:
        verdict = False
    else:
        verdict = True

    logging.debug(
        "is_daytime({}, {}) - {}"
        .format(str(location_lat), str(location_long), str(verdict)))

    return verdict

def get_icon_from_metoffice_weathercode(weathercode, is_daytime):
    icon_dict = {
                    0: "clearnight",  # Clear night
                    1: "skc",  # Sunny day
                    2: "partlycloudynight",  # Partly cloudy (night)
                    3: "sct",  # Partly cloudy (day)
                    4: "",  # Not used
                    5: "fg",  # Mist
                    6: "fg",  # Fog
                    7: "sct" if is_daytime else "partlycloudynight",  # Cloudy
                    8: "ovc",  # Overcast
                    9: "ra",  # Light rain shower (night)
                    10: "ra",  # Light rain shower (day)
                    11: "ra",  # Drizzle
                    12: "ra",  # Light rain
                    13: "ra",  # Heavy rain shower (night)
                    14: "ra",  # Heavy rain shower (day)
                    15: "ra",  # Heavy rain
                    16: "mix",  # Sleet shower (night)
                    17: "mix",  # Sleet shower (day)
                    18: "mix",  # Sleet
                    19: "rasn",  # Hail shower (night)
                    20: "rasn",  # Hail shower (day)
                    21: "rasn",  # Hail
                    22: "sn",  # Light snow shower (night)
                    23: "sn",  # Light snow shower (day)
                    24: "sn",  # Light snow
                    25: "sn",  # Heavy snow shower (night)
                    26: "sn",  # Heavy snow shower (day)
                    27: "sn",  # Heavy snow
                    28: "tsra",  # Thunder shower (night)
                    29: "tsra",  # Thunder shower (day)
                    30: "tsra",  # Thunder
                }

    icon = icon_dict[weathercode]
    logging.debug(
        "get_icon_by_weathercode({}) - {}"
        .format(weathercode, icon))

    return icon

def get_description_from_metoffice_weathercode(weathercode):
    description_dict = {
                            0: "Clear night",
                            1: "Sunny day",
                            2: "Partly cloudy",
                            3: "Partly cloudy",
                            4: "Not used",
                            5: "Mist",
                            6: "Fog",
                            7: "Cloudy",
                            8: "Overcast",
                            9: "Light rain shower",
                            10: "Light rain shower",
                            11: "Drizzle",
                            12: "Light rain",
                            13: "Heavy rain shower",
                            14: "Heavy rain shower",
                            15: "Heavy rain",
                            16: "Sleet shower",
                            17: "Sleet shower",
                            18: "Sleet",
                            19: "Hail shower",
                            20: "Hail shower",
                            21: "Hail",
                            22: "Light snow shower",
                            23: "Light snow shower",
                            24: "Light snow",
                            25: "Heavy snow shower",
                            26: "Heavy snow shower",
                            27: "Heavy snow",
                            28: "Thunder shower",
                            29: "Thunder shower",
                            30: "Thunder",
                        }
    description = description_dict[weathercode]

    logging.debug(
        "get_description_by_weathercode({}) - {}"
        .format(weathercode, description))

    return description.title()

# Get weather from MetOffice Weather DataHub
# https://metoffice.apiconnect.ibmcloud.com/metoffice/production/node/173
def get_weather():

    url = ("https://api-metoffice.apiconnect.ibmcloud.com/metoffice/production/v0/forecasts/point/daily?excludeParameterMetadata=false&includeLocationName=false&latitude={}&longitude={}"
            .format(location_lat, location_long))

    headers = {
        "X-IBM-Client-Id": client_id,
        "X-IBM-Client-Secret": client_secret,
        "accept": "application/json"
    }

    response_data = json.loads(requests.get(url, headers=headers).text)

    logging.debug(response_data)

    datahub_time = datetime.now().strftime("%Y-%m-%dT00:00Z")  # midnight of the current day

    for day_forecast in response_data["features"][0]["properties"]["timeSeries"]:
        if day_forecast["time"] == datahub_time:
            weather_data = day_forecast

    logging.debug("get_weather() - {}".format(weather_data))

    daytime = is_daytime(location_lat, location_long)
    weather_code = weather_data["daySignificantWeatherCode"] if daytime else weather_data["nightSignificantWeatherCode"]
    # { "temperatureMin": "2.0", "temperatureMax": "15.1", "icon": "mostly_cloudy", "description": "Cloudy with light breezes" }
    weather = {}
    weather["temperatureMin"] = weather_data["nightMinScreenTemperature"] #if self.units == "metric" else self.c_to_f(weather_data["nightMinScreenTemperature"])
    weather["temperatureMax"] = weather_data["dayMaxScreenTemperature"] #if self.units == "metric" else self.c_to_f(weather_data["dayMaxScreenTemperature"])
    weather["icon"] = get_icon_from_metoffice_weathercode(weather_code, daytime)
    weather["description"] = get_description_from_metoffice_weathercode(weather_code)
    logging.debug(weather)
    return weather
