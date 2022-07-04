from models import db, User, FavoriteLocations
from app import app

# create all tables
db.drop_all()
db.create_all()

# If table isnt empty then empty it
User.query.delete()
FavoriteLocations.query.delete()


#Add users

samuel = User.register('samuel.gonzalez', 'test123', 'samuel', 'gonzalez', 'samuel.gonzalez@test.com', 'Vineland', 'NJ', '08361')

sara = User.register('sara.smith', 'test123', 'sara', 'smith', 'sara.smith@test.com', 'Vineland', 'NJ', '08361')

mike = User.register('mike.maletta', 'test123', 'mike', 'maletta', 'mike.maletta@test.com', 'Vineland', 'NJ', '08361')

samuel_location_1 = FavoriteLocations.add_location('Vineland', 'New Jersey', samuel.username)

samuel_location_2 = FavoriteLocations.add_location('Millville', 'New Jersey', samuel.username)

samuel_location_3 = FavoriteLocations.add_location('Cape May', 'New Jersey', samuel.username)



# Add new users to session, so they'll persist
db.session.add(samuel)
db.session.add(sara)
db.session.add(mike)

db.session.commit()

db.session.add(samuel_location_1)
db.session.add(samuel_location_2)
db.session.add(samuel_location_3)

db.session.commit()