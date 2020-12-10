"""Seed file to make Sample Data For weather db"""

from models import City, db
from app import app

#Create all tables

db.drop_all()
db.create_all()

# Add Cities

London = City(name='London')
Seattle = City(name='Seattle')
Houston = City(name='Houston')

# Add new cities to session 
db.session.add(London)
db.session.add(Seattle)
db.session.add(Houston)

#Commit

db.session.commit()