'''bycrypt Application'''

from array import array
from crypt import methods
from dataclasses import dataclass
from distutils.log import Log
import weakref
from flask import Flask, redirect, render_template, request, session
from sqlalchemy import delete
from secret import secret_key
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from datetime import date
from forms import LoginForm, AddRegisterForm
from models import User, FavoriteLocations
from flask_bcrypt import Bcrypt
import requests
from forcast import weather_api, ExtractWeatherData


# this is initiate the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///weather'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = secret_key

# This contains the debug toolbar
# debug = DebugToolbarExtension(app)


bcrypt = Bcrypt()


# this will connect the app to the DB
connect_db(app)

# This will get todays date
todays_date = date.today() 

@app.route('/')
def homepage():
  '''This will contain all the pets that are currently posted on the application'''
  if session.get('username') is None:
    session['username'] = None

  if session.get('locations') is None: 
    session['locations'] = []

  if session.get('first_name') is None:
    session['first_name'] = None

  if session.get('last_name') is None:
    session['last_name'] = None
  
  if session.get('flash') is None:
    session['flash'] = False

  if session.get('flash_msg') is None:
    session['flash_msg'] = ''

  if session.get('home_city') is None:
    session['home_city'] = None
  
  if session.get('home_state') is None:
    session['home_state'] = None

  if session.get('home_zip') is None:
    session['home_zip'] = None

  if session.get('search_results') is None:
    session['search_results'] = None

  if session.get('email') is None:
    session['email'] = None

  
  if session.get('username') != None: 
    results = weather_api(f"{session['home_city']} {session['home_state']}")
    session['search_results'] = results
    return redirect('/weather_search')



  return render_template('home.html', first_name = session.get('first_name'), last_name = session.get('last_name'), username = session.get('username'), todays_date = todays_date)
  


@app.route('/login', methods=['POST', 'GET'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    username = User.query.get(form.username.data)
    stored_pw = form.password.data
    
    # Check to see if username and PW 
    # Match the DB and then redirect to secrets

    # bcrypt.check_password_hash(username.password, form.password.data)

    if username != None and bcrypt.check_password_hash(username.password, stored_pw):
      fav_locations = FavoriteLocations.query.filter_by(username = username.username).all()
      arr = []
      for location in fav_locations:
        arr.append(f"{location.city} {location.state}")

      session['username'] = username.username
      session['first_name'] = username.first_name
      session['last_name'] = username.last_name
      session['home_city'] = username.home_city
      session['home_state'] = username.home_state
      session['home_zip'] = username.home_zip
      session['flash'] = False
      session['flash_msg'] = ''
      session['locations'] = arr
      session['email'] = username.email

      return redirect('/')
    else:
      # ADD A Flask Flash Method
      session['flash'] = True
      session['flash_msg'] = 'Incorrect Username or Password. Please Try again.'
      return render_template('login.html', form = form, session = session)
  elif session['username'] != None:
    return redirect("/")
  else:
    return render_template('login.html', form = form, session = session)


@app.route('/register', methods=['POST', 'GET'])
def register():
  '''This will contain all the pets that are currently posted on the application'''
  form = AddRegisterForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    home_city = form.home_city.data
    home_state = form.home_state.data
    home_zip = form.home_zip.data

  
    # If youre not signed in the following code will run
    if session.get('username') == None:

        user = User.register(username, password, first_name, last_name, email, home_city, home_state, home_zip)

        db.session.commit()

        favorite_location = FavoriteLocations.add_location(home_city, home_state, username)

        db.session.commit()

        session['flash'] = False
        session['flash_msg'] = ''
        session['username'] = user.username
        session['first_name'] = user.first_name
        session['last_name'] = user.last_name
        session['locations'] = []
        session['home_city'] = user.home_city
        session['home_state'] = user.home_state
        session['home_zip'] = user.home_zip
        session['email'] = user.email
        return redirect('/')

    elif session.get('username' != None):
      user = User.update(session['username'], password, first_name, last_name, email, home_city, home_state, home_zip)

      db.session.commit()

      session['flash'] = False
      session['flash_msg'] = ''
      session['username'] = user.username
      session['first_name'] = user.first_name
      session['last_name'] = user.last_name
      session['locations'] = []
      session['home_city'] = user.home_city
      session['home_state'] = user.home_state
      session['home_zip'] = user.home_zip
      session['email'] = user.email
      
      
      return redirect('/account')

    
  else:
    return render_template('register.html', form = form, )




# This will let you log out
@app.route("/logout")
def logout():
    """Logout route."""
    if "username" in session:
      session.pop("username")
      session.pop('first_name')
      session.pop('last_name')
      session['locations'].clear()
      session.pop('home_city')
      session.pop('home_state')
      session.pop('home_zip')
      session.pop('email')
      session['flash'] = False
      session['flash_msg'] = ''
      
    return redirect("/")

@app.route('/search', methods=['POST'])
def search():
  address = request.form['address']
  if address == '':
    session['flash'] = False
    session['flash_msg'] = ''
    session['search_results'] = None
    return redirect('/')
  
  data = weather_api(address)

  if data.get('location') != None:
    session['flash'] = False
    session['flash_msg'] = ''
    session['search_results'] = data
    return redirect('/weather_search')
  else: 
    session['flash'] = True
    session['flash_msg'] = 'Please Enter a Valid Address or Zip Code'
    session['search_results'] = None
    return redirect('/')


@app.route('/weather_search')
def searched_weather():
  if session['search_results'] == None:
    return redirect('/')
  
  else:

    arr = []
    for day in session['search_results']['forecast']['forecastday']:
      arr.append(day)

    weather_data = ExtractWeatherData(session.get('search_results'))
    location = weather_data.location()
    icon = weather_data.weather_icon_url()
    temp = weather_data.temperature()
    current_condition = weather_data.current_condition()
    last_updated = weather_data.last_updated()
    feels_like = weather_data.feels_like()
    wind_mph = weather_data.wind_mph()
    wind_dirrection = weather_data.wind_dirrection()
    wind_gust = weather_data.wind_gust()
    precipitation = weather_data.precipitation_in()
    humidity = weather_data.humidity()
    uv = weather_data.uv()
    city = weather_data.city()
    state = weather_data.state()
    sunrise = weather_data.sunrise_3day()[0]
    sunset = weather_data.sunset_3day()[0]
    lat = weather_data.lat()
    lon = weather_data.lon()

    return render_template('weather_searched.html', 
    location = location, 
    icon = icon, 
    temp = temp, 
    current_condition = current_condition, 
    last_updated = last_updated, 
    feels_like = feels_like, 
    wind_mph = wind_mph,
    wind_dirrection = wind_dirrection,
    wind_gust = wind_gust,
    precipitation = precipitation, 
    humidity = humidity, 
    uv = uv, 
    city = city, 
    state = state, 
    sunrise = sunrise, 
    sunset = sunset, 
    lat = lat, 
    lon = lon, 
    arr = arr)



@app.route('/favorite_locations/<city>/<state>')
def favorite_locations(city, state):
  if session.get('username') != None and f"{city} {state}" not in session.get('locations'):
    session['locations'] = [*session['locations'], f"{city} {state}"]
    add_fav_location = FavoriteLocations().add_location(city, state, session['username'])
    db.session.commit()

  return redirect('/weather_search')




@app.route('/saved_location')
def saved_locations():
  
  if session.get('username') != None:
    arr = []
    for location in session['locations']:
      data = weather_api(location)
      extract = ExtractWeatherData(data)
      arr.append(extract)
      

    return render_template('locations.html', arr = arr)

  else:
    return redirect('/')



@app.route('/account', methods=["GET", 'POST'])
def account():

  form = AddRegisterForm()
  
  if form.validate_on_submit():
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    home_city = form.home_city.data
    home_state = form.home_state.data
    home_zip = form.home_zip.data

    user = User.update(session['username'], password, first_name, last_name, email, home_city, home_state, home_zip)
    print('success')
    db.session.commit()

    session['flash'] = False
    session['flash_msg'] = ''
    session['username'] = user.username
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['locations'] = []
    session['home_city'] = user.home_city
    session['home_state'] = user.home_state
    session['home_zip'] = user.home_zip
    session['email'] = user.email
  
    return redirect('/account')


  elif session.get('username') != None: 

    return render_template('account.html', 
    first_name = session['first_name'], 
    last_name = session['last_name'], 
    form = form, 
    username = session['username'], 
    email = session['email'], 
    home_city = session['home_city'], 
    home_state = session['home_state'], 
    home_zip = session['home_zip'])
    
  else: 
    return redirect('/')



@app.route('/delete_location', methods=["POST"])
def delete_location():
  resp_city = request.form['city']
  if session.get('username') != None: 
    FavoriteLocations.query.filter_by(username = session['username']).filter_by(city = resp_city).delete()
    db.session.commit()

    fav_locations = FavoriteLocations.query.filter_by(username = session['username']).all()
    arr = []
    for location in fav_locations:
      arr.append(f"{location.city} {location.state}")

    session['locations'] = arr

    return redirect('/saved_location')
  else:
    return redirect('/')