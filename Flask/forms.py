from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired
from wtforms import SelectField, SubmitField

class listRideForm:
    @staticmethod
    def form(ride)
        class F(FlaskForm): #variables you create here can be used in list-rides.html
        origin = StringField(default=ride.origin)
        destination = StringField(default=ride.destination)
        earliest_time = StringField (default=ride.earliest_time) #should not be a StringField- how should user do it?
        latest_time = StringField (default=ride.latest_time)
        seats_available = IntegerField(default=ride.seats_available #should I make this integer field?)
        gas_price = IntegerField(default=ride.gas_price)
        comments = StringField(default=ride.comments)
        save = SubmitField('Save')
