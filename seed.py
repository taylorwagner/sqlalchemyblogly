"""Seed file to make sample data for pets db."""

from models import User, db, Post
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

# Add posts
post1 = Post(title="Yes!!", content="I am so excited!", user_id=4)
post2 = Post(title="No!!", content="Please not me!", user_id=4)
post3 = Post(title="Maybe", content="I'll see what I can do", user_id=1)
post4 = Post(title="Sure", content="What does that even mean?", user_id=3)
post5 = Post(title="Love", content="God is love", user_id=8)
post6 = Post(title="Uncertainty", content="Who knows??", user_id=8)

# Add new objects to session, so they'll persist
db.session.add_all([post1, post2, post3, post4, post5, post6])

# Commit--otherwise, this never gets saved!
db.session.commit()