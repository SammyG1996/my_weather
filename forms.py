from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import PasswordInput


class LoginForm(FlaskForm):
  '''This will contain the from to add new pets'''

  username = StringField('Username', [InputRequired()])
  password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired()])


class AddRegisterForm(FlaskForm):
  '''This will contain the from to add new pets'''

  username = StringField('Username', [InputRequired()])
  password = StringField('Password', widget=PasswordInput(hide_value=False), validators=[InputRequired()])
  email = StringField('Email', validators=[InputRequired()])
  first_name = StringField('First Name', validators=[InputRequired()])
  last_name = StringField('Last Name', validators=[InputRequired()])
  home_city = StringField('Home City', validators=[InputRequired()])
  home_state = StringField('Home State Abbreviation', validators=[InputRequired(), Length(max=2)])
  home_zip = StringField('Home Zip', validators=[InputRequired()])

