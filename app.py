'''My Weather Application'''
from cgi import print_environ_usage
from flask import Flask, redirect, render_template, request, session, url_for
import flask
from sqlalchemy import delete
from urllib3 import Retry
from secret import secret_key
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension
from datetime import date
from forms import LoginForm, AddRegisterForm
from models import User, FavoriteLocations
from flask_bcrypt import Bcrypt
from forcast import weather_api, get_address_by_ip ,ExtractWeatherData
import os



# this will initiate the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:xIXhjC642d0EgTrdfmLW@containers-us-west-20.railway.app:6029/railway')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secret_key)

# This contains the debug toolbar
# debug = DebugToolbarExtension(app)

# This will initialiez the encryption for passwords
bcrypt = Bcrypt()


# this will connect the app to the DB
connect_db(app)

# This will get todays date
todays_date = date.today() 









@app.route('/')
def homepage():
  '''
  This will show the users home location when logged in, or it will show a prompt to login or register if not logged in
  However uses can still choose to search without being logged in
  '''

  # Below will initialize all the sessions that will be used in the application
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


  return render_template('home.html', todays_date = todays_date)
  



@app.route('/home_weather')
def home_weather():
  if session.get('username') != None: 
    results = weather_api(f"{session['home_city']} {session['home_state']}")
    session['search_results'] = results
    session['flash'] = False
    session['flash_msg'] = ''
    return redirect('/weather_search')
  else:
    return redirect('/')








@app.route('/login', methods=['POST', 'GET'])
def login():

  '''
  This will allow the user to access the login form and then redirect them to the homepage. 
  If the user is already looged in they will be redirected to the homepage
  '''
  form = LoginForm()

  # This will run if the form is validated
  if form.validate_on_submit():
    # First we get the username and password from the DB
    username = User.query.get(form.username.data)
    stored_pw = form.password.data

    # Then we compare the username and PW that was entered into the form with what is on the DB

    # If there is a match the user will get logged in by adding all the users non sensitive data into the session storage
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

      return redirect('/home_weather')
    
    # If there are not validated a message will be flashed telling them that their username or pw is wrong
    else:
      session['flash'] = True
      session['flash_msg'] = 'Incorrect Username or Password. Please Try again.'
      return render_template('login.html', form = form, session = session)
  
  # if the form doesnt validate and there is a username in the session storage then they will be redirected to the homepage
  elif session['username'] != None:
    return redirect("/")
  # Else they will be sent to the login page again
  else:
    return render_template('login.html', form = form, session = session)












@app.route('/register', methods=['POST', 'GET'])
def register():
  '''This will allow the user to register if they are not already registered'''
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

      # First we query the DB to see if the username is already in there
      check_user = User.query.get(form.username.data)

      # If the username exist we flash a message and redirect to the login page
      if check_user != None: 
        session['flash'] = True
        session['flash_msg'] = 'User already exists'
        return redirect('/login')

      # If the user doesnt exist then the following code will run registering the user and saving them to the DB
      user = User.register(username, password, first_name, last_name, email, home_city, home_state, home_zip)

      db.session.commit()

      # All the non sensitive data will be saved to session storage
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
      return redirect('/home_weather')

    # if the user is logged in then they will be redirected to the homepage 
    else:
      return redirect('/home_weather')

  # If the form doesnt validate they will be sent to the register page again
  else:
    return render_template('register.html', form = form, )













@app.route("/logout")
def logout():
  '''This will log the user out by clearing out everything in the session storage'''
  if "username" in session:
    session.pop("username")
    session.pop('first_name')
    session.pop('last_name')
    session['locations'].clear()
    session.pop('home_city')
    session.pop('home_state')
    session.pop('home_zip')
    session.pop('email')
    session['flash'] = True
    session['flash_msg'] = 'Login or Register to save your favorite locations!'
    
  return redirect("/")















@app.route('/search', methods=['GET', 'POST'])
def search():
  '''
  This will be the route that the search form submits to.
  It will either result in a redirect to the homepage if the form is submitted with nothing, 
  or it will make an API request with the submitted data. 

  If the data comes back with with valid data the user will be redirected to the '/weather_search' and the results from 
  the API will be saved in the session storage. 

  If the API comes back with None then a message will flash to the user saying to enter a valid address
  '''
  if flask.request.method == 'POST':
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
      if session.get('username') == None:
        session['flash'] = True
        session['flash_msg'] = 'Login or Register to save your favorite locations!'
      else:
        session['flash'] = False
        session['flash_msg'] = ''


      return redirect('/weather_search')
    else: 
      session['flash'] = True
      session['flash_msg'] = 'Please Enter a Valid Address or Zip Code'
      session['search_results'] = None
      return redirect('/')

  else:
    args = request.args
    ip = args.to_dict().get('q')
    data = weather_api(ip)
    session['search_results'] = data
    return data













@app.route('/weather_search')
def searched_weather():
  '''This route will check the search results from the API that is stored in the session storage a redirect or render accordingly'''

  # if there is nothing stored in the session storage then the user is redirected home
  if session.get('search_results') == None:
    return redirect('/')
  
  # If there is something then the following code runs
  else:
    # An empty array is created and a for loop goes through the search results in the session storage  
    # to get the 3 day forecast info. The array is then passes as an argument to the jinja template
    arr = []
    for day in session['search_results']['forecast']['forecastday']:
      arr.append(day)

    # The below code will then retrive the individual bits of info from the stored search results data
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
    country = weather_data.country()
    session['flash'] = False
    session['flash_msg'] = ''

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
    arr = arr, 
    country = country)













@app.route('/favorite_locations/<city>/<state>')
def favorite_locations(city, state):
  '''
  If the user is logged in then the follwoing code will save the submitted location to 
  the favorite locations DB. 
  '''
  if session.get('username') != None and f"{city} {state}" not in session.get('locations'):
    session['locations'] = [*session['locations'], f"{city} {state}"]
    add_fav_location = FavoriteLocations().add_location(city, state, session['username'])
    session['flash'] = True
    session['flash_msg'] = 'Added Location to saved locations'
    db.session.commit()

  return redirect('/weather_search')












@app.route('/saved_location')
def saved_locations():
  '''
  This route will show all of the saved favorite locations if the user is logged in
  '''
  if session.get('username') != None:
    arr = []
    for location in session['locations']:
      data = weather_api(location)
      extract = ExtractWeatherData(data)
      arr.append(extract)
      session['flash'] = False
      session['flash_msg'] = ''
      

    return render_template('locations.html', arr = arr)

  else:
    session['flash'] = False
    session['flash_msg'] = ''
    return redirect('/')



@app.route('/account', methods=["GET", 'POST'])
def account():
  '''
  This route will show the accout information and allow you to edit it. 

  There is also a POST method to then save the new information to the DB
  '''

  # This will instantiate the form
  form = AddRegisterForm()
  
  # If the form validates the following will run as a POST request
  if form.validate_on_submit():
    # All of the data from the form will be extracted
    password = form.password.data
    email = form.email.data
    first_name = form.first_name.data
    last_name = form.last_name.data
    home_city = form.home_city.data
    home_state = form.home_state.data
    home_zip = form.home_zip.data

    # A function will then update the DB with the new information and update the session storage
    user = User.update(session['username'], password, first_name, last_name, email, home_city, home_state, home_zip)

    session['flash'] = False
    session['flash_msg'] = ''
    session['username'] = user.username
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['home_city'] = user.home_city
    session['home_state'] = user.home_state
    session['home_zip'] = user.home_zip
    session['email'] = user.email
    session['flash'] = True
    session['flash_msg'] = 'Account Information Updated'

    db.session.commit()

    return redirect('/account')

  # This will then handle the GET request and return the form with the acct info to update
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
    
  # However is the user is not logged in then they will just be redirected to the homepage
  else: 
    return redirect('/')



@app.route('/delete_location', methods=["POST"])
def delete_location():
  '''This will handle removing a location from your favorites list.'''
  resp_city = request.form['city']
  # If the user is logged in we retrive the city to delete from the DB and remove it
  if session.get('username') != None: 
    FavoriteLocations.query.filter_by(username = session['username']).filter_by(city = resp_city).delete()
    db.session.commit()
    # Then we retrive the refreshed list from the DB and reassign it to the session storage
    fav_locations = FavoriteLocations.query.filter_by(username = session['username']).all()
    arr = []
    for location in fav_locations:
      arr.append(f"{location.city} {location.state}")

    session['locations'] = arr
    session['flash'] = True
    session['flash_msg'] = 'Location Deleted'

    return redirect('/saved_location')
  else:
    return redirect('/')