from sqlalchemy import sql, orm
from app import db

class Rideshare_user(db.Model):
    __tablename__ = 'rideshare_user' 
    netid = db.Column('netid', db.String(7), primary_key=True)
    name = db.Column('name', db.String(50))
    duke_email = db.Column('duke_email', db.String(50)) 
    phone_number = db.Column('name', db.Integer()) #from reading about this online, I think that it should convert to big num itself
    affiliation = db.Column('affiliation', db.String(50)) #Jane said we don't make this a drop down menu here, we do it later in forms
    school = db.Column('school', db.String(50))
    password = db.Column('password', db.String(50))


class Driver(db.Model):
    __tablename__ = 'driver'
    netid = db.Column('netid', db.String(20), db.ForeignKey('rideshare_user.netid'), rimary_key=True)
    license_no = db.Column('license_no', db.Integer())
    license_plate_no = db.Column('license_plate_no', db.String(10))
    plate_state = db.Column('plate_state', db.String(3))

class Ride(db.Model):
    __tablename__ = 'ride'
    ride_no = db.Column('ride_no', db.Integer(), primary_key=True) #How do I make this increment each time?
    origin = db.Column('origin', db.String(100))
    destination = db.Column('destination', db.String(100)) #how to I make not equal origin? triggers?- piazza
    driver_netid = db.Column('driver_netid', db.String(10), ForeignKey('driver.netid'))
    earliest_time= db.Column('earliest_time', db.DateTime) 
    latest_time= db.Column('latest_time', db.DateTime)
    seats_available= db.Column('seats_available', db.Integer())
    gas_price = db.Column('gas_price', db.Integer())
    comments = db.Column('comments', db.String(500))


class Reserve(db.Model):
    __tablename__ = 'reserve'
    id = odm.CompositeIdField('rider_netid', 'ride_no') #might be wrong- trying to make both primary key?
    rider_netid = db.Column('rider_netid', ForeignKey('rideshare_user.netid')) #do I have to make separate line like in sql?
    ride_no = db.Column('ride_no', ForeignKey('ride.ride_no'))
    seats_needed = db.Column('seats_needed', db.Integer())
    note = db.Column('note', db.String(150))


    ##why do they do drinker this way- just keeping here to understand. Is this how triggers are done
class Drinker(db.Model):
    __tablename__ = 'drinker'
    name = db.Column('name', db.String(20), primary_key=True)
    address = db.Column('address', db.String(20))
    likes = orm.relationship('Likes')
    frequents = orm.relationship('Frequents')
    @staticmethod
    def edit(old_name, name, address, beers_liked, bars_frequented):
        try:
            db.session.execute('DELETE FROM likes WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('DELETE FROM frequents WHERE drinker = :name',
                               dict(name=old_name))
            db.session.execute('UPDATE drinker SET name = :name, address = :address'
                               ' WHERE name = :old_name',
                               dict(old_name=old_name, name=name, address=address))
            for beer in beers_liked:
                db.session.execute('INSERT INTO likes VALUES(:drinker, :beer)',
                                   dict(drinker=name, beer=beer))
            for bar, times_a_week in bars_frequented:
                db.session.execute('INSERT INTO frequents'
                                   ' VALUES(:drinker, :bar, :times_a_week)',
                                   dict(drinker=name, bar=bar,
                                        times_a_week=times_a_week))
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
