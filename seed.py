"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
taylor = User(first_name="Taylor", last_name="Wagner", image_url="https://images.unsplash.com/photo-1618496899001-b58ebcbeef26?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=400&q=80")
santana = User(first_name="Santana", last_name="Porter", image_url="https://images.unsplash.com/photo-1621605186702-53a6b4cde199?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=334&q=80")
leonard = User(first_name="Leonard", last_name="Porter", image_url="https://images.unsplash.com/photo-1621266454419-45aefdd403ce?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=334&q=80")
megan = User(first_name="Megan", last_name="Porter")

# Add new objects to session, so they'll persist
db.session.add(taylor)
db.session.add(santana)
db.session.add(leonard)
db.session.add(megan)

# Commit--otherwise, this never gets saved!
db.session.commit()