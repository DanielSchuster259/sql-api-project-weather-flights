# Get weather data from August 2005 (during Hurricane Katrina), from weather stations nearest to 
# lat and lon given as input variables

def get_katrina_weather_data(lat, lon, granularity='daily'):
    
    import requests
    import os
    import pandas as pd
    from dotenv import load_dotenv
    load_dotenv()

    url = (f"https://meteostat.p.rapidapi.com/point/{granularity}")

    querystring = {
        "lat":lat,
        "lon":lon,
        "start":"2005-08-01",
        "end":"2005-08-31",
        "alt":"2"
        }

    headers = {
        "X-RapidAPI-Key": os.getenv('rapid_api_key'),
	    "X-RapidAPI-Host": os.getenv('rapid_api_host')
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    weather_katrina = response.json()
    weather_katrina_data = weather_katrina['data']                               # Retrieving only the nested data dict from .json file -> omitting Station information
    weather_katrina_data_norm = pd.json_normalize(weather_katrina_data, sep="_") # Flattening data and convert to dataframe

    return weather_katrina_data_norm


def clean_hourly_data(df, airport_code):

    df.drop(columns=['dwpt', 'rhum', 'wdir', 
                     'snow', 'tsun', 'wpgt', 
                     'coco', 'prcp'], axis=1, 
                     inplace=True)
    df.rename(columns={'time' : 'date', 
                       'temp' : 'temp_celsius', 
                       'wspd' : 'wind_speed_kph', 
                       'pres' : 'air_pressure_hPa'}, 
                       inplace=True)

    airport_codes = [airport_code] * len(df)
    df['airport_code'] = airport_codes

    return df

def clean_daily_data(df, airport_code):

    df.drop(columns=['wdir', 'snow', 'tsun',       # Dropping columns that are unnecessary 
                     'wpgt', 'prcp', 'tmin',       # or have 0 Non-Null values
                     'tmax'], axis=1, 
                      inplace=True)
    df.rename(columns={'time' : 'date', 
                       'temp' : 'temp_celsius',         # Renaming columns
                       'wspd' : 'wind_speed_kph', 
                       'pres' : 'air_pressure_hPa', 
                       'tavg' : 'avg_temp_celsius'}, 
                       inplace=True, 
                       errors='ignore')

    airport_codes = [airport_code] * len(df)            # Creating a new column with airport code
    df['airport_code'] = airport_codes

    return df