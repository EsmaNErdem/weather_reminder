from models import db, User
from app import app
from flask import session

# Create all tables
db.drop_all()
db.create_all()
db.session.close()