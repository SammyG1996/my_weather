from flask import jsonify
import requests
api_key = 'fc398ea010514d839df201324220207'



def weather_api(location):

     resp = requests.get(
               "https://api.weatherapi.com/v1/forecast.json",
               params={"key": api_key, "q": location, 'days': 7, 'alerts': 'yes'}
          )
     # Converts the response into a Python Dictionay
     data = resp.json()

     # This will return a Python Dictionary of the Data. I can then use this in
     # The following  functions to extract the data that I need
     return data

def get_address_by_ip():
    resp = requests.get("https://api.ipify.org?format=json")
    data = resp.json()
    return data['ip']


class ExtractWeatherData:
  def __init__(self, data):
    self.data = data

  # These Funtions are for the current weather ------------------------------------------------------

  def location(self):
      return f"{self.data['location']['name']} {self.data['location']['region']} {self.data['location']['country']}"

  def current_condition(self):
      return f"{self.data['current']['condition']['text']}"

  def last_updated(self):
      return f"{self.data['current']['last_updated']}"

  def weather_icon_url(self):
      return f"{self.data['current']['condition']['icon']}"

  def temperature(self):
      return f"{self.data['current']['temp_f']}"

  def feels_like(self):
      return f"{self.data['current']['feelslike_f']}"

  def is_it_daytime(self):
      if self.data['current']['is_day'] == 1:
            return True
      else:
            return False

  def wind_mph(self):
      return f"{self.data['current']['wind_mph']}"

  def wind_dirrection(self):
      return f"{self.data['current']['wind_dir']}"

  def wind_gust(self):
      return f"{self.data['current']['gust_mph']}"

  def uv(self):
      return f"{self.data['current']['uv']}"

  def humidity(self):
      return f"{self.data['current']['humidity']}"

  def precipitation_in(self): 
      return f"{self.data['current']['precip_in']}"

  def local_date_time(self):
      return f"{self.data['location']['localtime']}"

  def city(self): 
    return f"{self.data['location']['name']}"

  def state(self): 
    return f"{self.data['location']['region']}"

  def country(self):
    return f"{self.data['location']['country']}"

  def lat(self):
    return f"{self.data['location']['lat']}"

  def lon(self):
    return f"{self.data['location']['lon']}"

  

  # ---------------------------------------------------------------------------------------

  # These functions are for the 3 day forecast and will return an array containing the 3 days worth of information

  def date_3day(self): 
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['date'])
    return arr

  def max_temp_3day(self): 
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['day']['maxtemp_f'])
    return arr

  def min_temp_3day(self): 
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['day']['mintemp_f'])
    return arr

  def condition_3day(self): 
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['day']['condition']['text'])
    return arr

  def icon_3day(self): 
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['day']['condition']['icon'])
    return arr


    # --------------------------------------------------------------------

    # This will be for the sunrise and sunset and will return an array with 3 days worth of data

  def sunrise_3day(self): 
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['astro']['sunrise'])
    return arr

  def sunset_3day(self):
    forecastday = self.data['forecast']['forecastday']
    arr = []
    for day in forecastday:
      arr.append(day['astro']['sunset'])
    return arr