from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, validators, SubmitField, SelectField, ValidationError, DecimalField, DateTimeField
from wtforms_components import TimeField, DateRange
from wtforms.validators import InputRequired, Length, NumberRange, Regexp, Email, DataRequired, Optional
from wtforms.fields.html5 import DateTimeLocalField, DateField
from app import db
import models
import datetime

class NotEqualTo(object):  # --> Change to 'NotEqualTo'
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data == other.data:  #  --> Change to == from !=
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Destination must not be equal to origin.')

            raise ValidationError(message % d)
            

class GreaterThan(object):  # --> Change to 'GreaterThan'
    """
    Compares the values of two fields.

    :param fieldname:
        The name of the other field to compare to.
    :param message:
        Error message to raise in case of a validation error. Can be
        interpolated with `%(other_label)s` and `%(other_name)s` to provide a
        more helpful error.
    """
    def __init__(self, fieldname, message=None):
        self.fieldname = fieldname
        self.message = message

    def __call__(self, form, field):
        try:
            other = form[self.fieldname]
        except KeyError:
            raise ValidationError(field.gettext("Invalid field name '%s'.") % self.fieldname)
        if field.data < other.data:  #  --> Change to <= from !=
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Invalid date/time entry')

            raise ValidationError(message % d)
            
class RegisterFormFactory(FlaskForm):
    netid = StringField("NetID:", validators = [InputRequired(message='You must enter your NetID'), Length(min=4, max=7, message='Your NetID must be between 4 to 7 characters')])
    name = StringField("Name:", validators = [InputRequired(message='You must enter your name'), Length(min=5, max=256, message='Your name must be between 5 to 256 characters')])
    duke_email = StringField("Duke Email:", validators = [InputRequired(message='You must enter your Duke email'), Email(message='You must enter a valid email address'), Length(min=10, max=256, message='Your email must be between 10 to 256 characters'), Regexp('^[a-zA-Z0-9]+@duke.edu$', message = 'Please enter a valid Duke email address')])
    phone_number = IntegerField("Phone Number:", validators = [InputRequired(message='You must enter a valid phone number')])
    password = PasswordField("Password:", validators = [InputRequired(message='You must enter a password'), Length(min=5, max=256, message='Your password must be between 5 to 256 characters')])
    affiliation_sel = SelectField("Affiliation:", validators = [InputRequired(message='You must select your affiliation')], choices = [('Graduate', 'Graduate'), ('Undergraduate', 'Undergraduate')])
    school = SelectField("School:", validators = [InputRequired(message='You must enter your school')], choices = [('Pratt', 'Pratt'), ('Trinity', 'Trinity'), ('Fuqua', 'Fuqua'), ('Law', 'Law'), ('Medicine', 'Medicine'), ('Nicolas', 'Nicolas'), ('Nursing', 'Nursing'), ('Other', 'Other')])
    submit = SubmitField("Submit")      

class RegisterDriverFormFactory(FlaskForm):
    license_no = StringField("License Number", validators = [InputRequired(message='You must enter your license number'), Length(min=5, max=50, message='You must enter a license plate number that is between 5 to 50 characters')])
    license_plate_no = StringField("License Plate Number", validators = [InputRequired(message='You must enter your license plate number'), Length(min=2, max=8, message='You must enter a license plate number between 2 to 8 characters')])
    plate_state = StringField("State", validators = [InputRequired(message='You must enter the state of your license plate'), Length(min=2, max=2, message='Your license plate state must be your state abbreviation'), Regexp('^(?-i:A[LKSZRAEP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$', message='Your license plate state must be your state abbreviation')])
    submit = SubmitField("Submit")

class SearchFormFactory(FlaskForm):
    start_city = SelectField("Start City", validators = [InputRequired(message='You must select an origin')])
    end_city = SelectField("Destination") #may need coerce=unicode for this and line above
    #need to add date picker
    #need to add start time picker
    #need to add end time picker
    spots_needed = IntegerField("Spots Needed")
    submit = SubmitField("Search")
                                        
class ListRideFormFactory(FlaskForm):
    current_date = DateField('Current Date', default=datetime.date.today(), format='%Y-%m-%d', validators = [DataRequired()])
    destination = SelectField("Destination City:", validators = [InputRequired(message='You must select a destination city'), NotEqualTo('origin_city')], choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PN', 'Philadelphia, PN'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')])
    origin_city = SelectField("Origin City:", coerce=str, choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PN', 'Philadelphia, PN'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')])
    driver_netid = StringField("Driver NetID:", validators = [InputRequired(message='You must enter your driver netID'), Length(min=4, max=7, message='Your NetID must be between 4 to 7 characters')])
    date = DateField("Departure Date:", validators=[InputRequired(message='Please enter departure date'), GreaterThan('current_date')], format='%Y-%m-%d')
    earliest_departure = TimeField("Earliest Time of Departure:", validators=[InputRequired(message='Please enter the earliest time of departure')], format='%H:%M')
    latest_departure = TimeField("Latest Date/Time of Departure:", validators=[InputRequired(message='Please enter the latest date/time of departure'), GreaterThan('earliest_departure')], format='%H:%M')
    seats_available = IntegerField("Number of Seats Available:", validators = [InputRequired(message='You must enter the number of seats available')])
    gas_price = DecimalField("Gas Price per Person:", places=2, rounding=None, validators=[Optional()])
    comments = StringField("Comments:")
    submit = SubmitField("Submit")
