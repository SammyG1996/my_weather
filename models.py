from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import false, null
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy()

# This is a method that you will be able to call in the app.py file. It will allow you to initiate the connction to the database.
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    # This will create a new user in the db
    __tablename__ = 'user'
    
    username = db.Column(db.String(20), primary_key=True, unique=True, autoincrement=False)

    password = db.Column(db.String(), nullable=False)

    email = db.Column(db.String(50), unique=True, nullable=False)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    home_city = db.Column(db.String(), nullable=False)

    home_state = db.Column(db.String(), nullable=False)

    home_zip = db.Column(db.String(), nullable=False)

    @classmethod
    def register(cls, username, password, first_name, last_name, email, home_city, home_state, home_zip):
        """Register a user, hashing their password."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            first_name=first_name,
            last_name=last_name,
            email=email,
            home_city = home_city, 
            home_state = home_state, 
            home_zip = home_zip
        )

        db.session.add(user)
        return user

    def update(session_username, new_password, new_first_name, new_last_name, new_email, new_home_city, new_home_state, new_home_zip):
        hashed = bcrypt.generate_password_hash(new_password)
        hashed_utf8 = hashed.decode("utf8")

        user = User.query.get(session_username)

        user.password = hashed_utf8
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        user.home_city = new_home_city
        user.home_state = new_home_state
        user.home_zip = new_home_zip

        db.session.add(user)
        return user


class FavoriteLocations(db.Model):
    __tablename__ = 'favorite_locations'

    id = db.Column(db.Integer(), primary_key=True)

    city = db.Column(db.String(), nullable=False)

    state = db.Column(db.String(), nullable=False)

    username = db.Column(db.String(20), db.ForeignKey('user.username'))

    # This will add a relationship between the two databases
    user = db.relationship('User', backref='post')

    @classmethod
    def add_location(cls, city, state, username):
        user = cls(
            city = city,
            state = state,
            username=username
        )
        db.session.add(user)
        return user
