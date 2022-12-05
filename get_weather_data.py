# Get weather data from August 2005 (during Hurricane Katrina), from weather stations nearest to 
# lat and lon given as input variables

def get_katrina_weather_data(lat, lon):
    
    from dotenv import load_dotenv
    load_dotenv()

    import requests

    url = "https://meteostat.p.rapidapi.com/point/hourly"

    querystring = {"lat":lat,"lon":lon,"start":"2005-08-01","end":"2005-08-31","alt":"2"}

    headers = {
	    "X-RapidAPI-Key": os.getenv('rapid_api_key'),
	    "X-RapidAPI-Host": os.getenv('rapid_api_host')
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    # Import json package
    import json
    import pandas as pd

    weather_katrina = response.json()

    weather_katrina_data = weather_katrina['data']

    weather_katrina_data_norm = pd.json_normalize(weather_katrina_data, sep="_")

    return weather_katrina_data_norm