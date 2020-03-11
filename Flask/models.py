from sqlalchemy import sql, orm
from app import db

class Rideshare_user(db.Model):
    __tablename__ = 'rideshare_user' 
    netid = db.Column('netid', db.String(7), primary_key=True)
    name = db.Column('name', db.String(50))
    duke_email = db.Column('duke_email', db.String(50)) 
    phone_number = db.Column('phone_number', db.Integer()) #from reading about this online, I think that it should convert to big num itself
    affiliation = db.Column('affiliation', db.String(50)) #Jane said we don't make this a drop down menu here, we do it later in forms
    school = db.Column('school', db.String(50))
    password = db.Column('password', db.String(50))
    
class Driver(db.Model):
    __tablename__ = 'driver'
    netid = db.Column('netid', db.String(20), primary_key=True)
    license_no = db.Column('license_no', db.Integer())
    license_plate_no = db.Column('license_plate_no', db.String(10))
    plate_state = db.Column('plate_state', db.String(3))
