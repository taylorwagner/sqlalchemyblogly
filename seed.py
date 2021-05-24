"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
taylor = User(first_name="Taylor", last_name="Wagner", image_url="https://unsplash.com/photos/y_rjtoDFiA8")
santana = User(first_name="Santana", last_name="Porter", image_url="https://unsplash.com/photos/e__ERq5W5-w")
leonard = User(first_name="Leonard", last_name="Porter", image_url="https://unsplash.com/photos/Dj-p9J6JlYQ")
megan = User(first_name="Megan", last_name="Porter")

# Add new objects to session, so they'll persist
db.session.add(taylor)
db.session.add(santana)
db.session.add(leonard)
db.session.add(megan)

# Commit--otherwise, this never gets saved!
db.session.commit()