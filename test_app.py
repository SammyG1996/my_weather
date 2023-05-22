from sqlalchemy import extract
import app
from flask import session
from forcast import weather_api, ExtractWeatherData
from unittest import TestCase 

class AppTestCase(TestCase): 
  def test_location_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    location = extract.location()
    # This checks to see if the extracter returns the expected str
    self.assertEqual(location, 'Vineland New Jersey United States of America')

  def test_current_condition_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    current_condition = extract.current_condition()
    # This checks to see if the extracter returns the expected str
    self.assertEqual(type(current_condition), str)

  def test_last_updated_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    last_updated = extract.last_updated()
    # This checks to see if the extracter returns something
    self.assertNotEqual(last_updated, None)

  def test_weather_icon_url_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    weather_icon_url = extract.weather_icon_url()
    # This checks to see if the extracter returns a url
    self.assertIn('cdn.weatherapi.com', weather_icon_url)

  def test_temperature_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    temperature = extract.temperature()
    # This checks to see if the extracter returns something
    self.assertNotEqual(temperature, None)

  def test_feels_like_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    feels_like = extract.feels_like()
    # This checks to see if the extracter returns something
    self.assertNotEqual(feels_like, None)

  def test_is_it_daytime_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    is_it_daytime = extract.is_it_daytime()
    # This checks to see if the extracter returns a Boolean of True or False
    self.assertEqual(True or False, is_it_daytime)

  def test_wind_mph_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    wind_mph = extract.wind_mph()
    # This checks to see if the extracter returns something
    self.assertNotEqual(wind_mph, None)

  def test_wind_dirrection_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    wind_dirrection = extract.wind_dirrection()
    # This checks to see if the extracter returns something
    self.assertNotEqual(wind_dirrection, None)

  def test_wind_gust_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    wind_gust = extract.wind_gust()
    # This checks to see if the extracter returns something
    self.assertNotEqual(wind_gust, None)

  def test_uv_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    uv = extract.uv()
    # This checks to see if the extracter returns something
    self.assertNotEqual(uv, None)

  def test_humidity_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    humidity = extract.humidity()
    # This checks to see if the extracter returns something
    self.assertNotEqual(humidity, None)

  def test_precipitation_in_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    precipitation_in = extract.precipitation_in()
    # This checks to see if the extracter returns something
    self.assertNotEqual(precipitation_in, None)

  def test_city_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    city = extract.city()
    # This checks to see if the extracter returns something
    self.assertEqual(city, 'Vineland')

  def test_state_extracter(self): 
    data = weather_api('Vineland NJ')
    extract = ExtractWeatherData(data)
    state = extract.state()
    # This checks to see if the extracter returns something
    self.assertEqual(state, 'New Jersey')