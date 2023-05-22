from flask import jsonify
import requests
api_key = 'fc398ea010514d839df201324220207'



def weather_api(location):

     resp = requests.get(
               "https://api.weatherapi.com/v1/current.json",
               params={"key": api_key, "q": location}
          )
     # Converts the response into a Python Dictionay
     data = resp.json()

     # This will return a Python Dictionary of the Data. I can then use this in
     # The following  functions to extract the data that I need
     return data

     

def current_condition(data):
     return f"{data['current']['condition']['text']}"

def weather_icon_url(data):
     return f"{data['current']['condition']['icon']}"

def location(data):
     return f"{data['location']['name']} {data['location']['region']} {data['location']['country']}"

def temperature(data):
     return f"{data['current']['temp_f']}"

def feels_like(data):
     return f"{data['current']['feelslike_f']}"

def is_it_daytime(data):
     if data['current']['is_day'] == 1:
          return True
     else:
          return False

def wind_mph(data):
     return f"{data['current']['wind_mph']}"

def wind_dirrection(data):
     return f"{data['current']['wind_dir']}"

def wind_gust(data):
     return f"{data['current']['gust_mph']}"

def uv(data):
     return f"{data['current']['uv']}"

def humidity(data):
     return f"{data['current']['humidity']}"

def precipitation_in(data): 
     return f"{data['current']['precip_in']}"

def local_date_time(data):
     return f"{data['location']['localtime']}"