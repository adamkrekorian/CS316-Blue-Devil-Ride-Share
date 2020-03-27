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

class Ride(db.Model):
    __tablename__= 'ride'
    ride_no = db.Column('ride_no', db.Integer(), primary_key = True)
    origin = db.Column('origin', db.String(100))
    destination = db.Column('destination', db.String(100))
    driver_netid = db.Column('driver_netid', db.String(7))
    date = db.Column('date', db.Date())
    earliest_time = db.Column('earliest_time', db.Time())
    latest_time = db.Column('latest_time', db.Time())
    seats_available = db.Column('seats_available', db.Integer())
    gas_price = db.Column('gas_price', db.Integer())
    comments = db.Column('comments', db.String(500))

class Reserve(db.Model):
    __tablename__= 'reserve'
    #commented portions are wrong
    #id = odm.CompositeIdField('ride_no', 'rider_netid')
    # ride_no and rider_netid need to be foreign keys from the other tables
    # need a reserve id or something that increments to track reservations
    ride_no = db.Column('ride_no', db.Integer(), primary_key=True)
    rider_netid = db.Column('rider_netid', db.String(7), primary_key= True)
    seats_needed = db.Column('seats_needed', db.Integer())
    note = db.Column('note', db.String(500)) #create foreign keys
    #ride_no = db.Column('ride_no', db.Integer(), FOREIGN KEY(ride_no) REFERENCES Ride(ride_no))
    #rider_netid = db.Column('rider_netid', db.String(7), FOREIGN KEY(rider_netid) REFERENCES Rideshare_user(netid))