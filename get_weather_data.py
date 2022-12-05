# Get weather data from August 2005 (during Hurricane Katrina), from weather stations nearest to 
# lat and lon given as input variables

def get_katrina_weather_data(lat, lon):
    
    from dotenv import load_dotenv
    load_dotenv()

    import requests
    import os

    url = "https://meteostat.p.rapidapi.com/point/daily"

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

    #display(weather_katrina)

    weather_katrina_data = weather_katrina['data']

    weather_katrina_data_norm = pd.json_normalize(weather_katrina_data, sep="_")

    return weather_katrina_data_norm


def clean_hourly_data(df, airport_code):

    df.drop(columns=['dwpt', 'rhum', 'wdir', 'snow', 'tsun', 'wpgt', 'coco', 'prcp'], axis=1)
    df.rename(columns={'time' : 'date', 'temp' : 'temp_celsius', 'wspd' : 'wind_speed_kph', 'pres' : 'air_pressure_hPa'}, inplace=True)

    airport_codes = [airport_code] * len(df)
    df['airport_code'] = airport_codes

    return df

def clean_daily_data(df, airport_code):

    df = df.drop(columns=['wdir', 'snow', 'tsun', 'wpgt', 'prcp', 'tmin', 'tmax'], axis=1)
    df.rename(columns={'time' : 'date', 'temp' : 'temp_celsius', 'wspd' : 'wind_speed_kph', 'pres' : 'air_pressure_hPa', 'tvag' : 'avg_temp_celsius'}, inplace=True)

    airport_codes = [airport_code] * len(df)
    df['airport_code'] = airport_codes

    return df