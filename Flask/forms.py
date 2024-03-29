from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, HiddenField, IntegerField, PasswordField, validators, SubmitField, SelectField, ValidationError, DecimalField, DateTimeField
from wtforms_components import TimeField, DateRange
from wtforms.validators import InputRequired, Length, NumberRange, Regexp, Email, DataRequired, Optional, EqualTo, ValidationError
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

class EqualTo(object):  #might not be done correctly!!
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
        if field.data != other.data:  #  --> Change to == from !=
            d = {
                'other_label': hasattr(other, 'label') and other.label.text or self.fieldname,
                'other_name': self.fieldname
            }
            message = self.message
            if message is None:
                message = field.gettext('Password and confirm password must be equal.')

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

def school_choices(affiliation):
    """
    return a list containing school choices based on the given affiliation

    used to limit the choice of schools to those related to the current affiliation
    """
    if affiliation == 'Undergraduate':
        choices = [('Pratt', 'Pratt'), ('Trinity', 'Trinity')]
        return(choices)
    elif affiliation == 'Graduate':
        choices = [('Fuqua', 'Fuqua'), ('Law', 'Law'), ('Medicine', 'Medicine'), ('Nicholas', 'Nicholas'), ('Nursing', 'Nursing'), ('Other', 'Other')]
        return(choices)
    else:
        return [('Please select your affiliation.')]
 
class RegisterFormFactory(FlaskForm):
    netid = StringField("NetID:", validators = [InputRequired(message='You must enter your NetID'), Length(min=4, max=7, message='Your NetID must be between 4 to 7 characters'), Regexp('^[a-zA-Z]{2,3}\d{2,3}$', message = 'Please enter a valid netid.')])
    name = StringField("Name:", validators = [InputRequired(message='You must enter your name'), Length(min=5, max=50, message='Your name must be between 5 to 50 characters')])
    duke_email = StringField("Duke Email:", validators = [InputRequired(message='You must enter your Duke email'), Email(message='You must enter a valid email address'), Length(min=10, max=256, message='Your email must be between 10 to 256 characters'), Regexp('^[a-zA-Z0-9]+@duke.edu$', message = 'Please enter a valid Duke email address')])
    #phone number should be a string field so you can check it's length
    phone_number = IntegerField("Phone Number:", validators = [InputRequired(message='You must enter a valid phone number')])
    password = PasswordField("Password:", validators = [InputRequired(message='You must enter a password'), Length(min=5, max=256, message='Your password must be between 5 to 256 characters'), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password:", validators = [InputRequired(message='You must confirm your password')])
    affiliation_sel = SelectField("Affiliation:", validators = [InputRequired(message='You must select your affiliation')], choices = [('Graduate', 'Graduate'), ('Undergraduate', 'Undergraduate')])
    school = SelectField("School:", validators = [InputRequired(message='You must enter your school')], choices = [('Pratt', 'Pratt'), ('Trinity', 'Trinity'), ('Fuqua', 'Fuqua'), ('Law', 'Law'), ('Medicine', 'Medicine'), ('Nicholas', 'Nicholas'), ('Nursing', 'Nursing'), ('Other', 'Other')])
    #school = SelectField("School:", validators = [InputRequired(message='You must enter your school')], choices = school_choices(affiliation_sel))
    submit = SubmitField("Submit")      

class RegisterDriverFormFactory(FlaskForm):
    #NOTE: should try to do it the top 3 ways later with java script and with regexp
    license_no = StringField("License Number", validators = [InputRequired(message='You must enter your license number'), Length(min=5, max=20, message='You must enter a license plate number that is between 5 to 20 characters')])
    license_plate_no = StringField("License Plate Number", validators = [InputRequired(message='You must enter your license plate number'), Length(min=2, max=10, message='You must enter a license plate number between 2 to 10 characters')])
    #plate_state = StringField("State", validators = [InputRequired(message='You must enter the state of your license plate'), Length(min=2, max=2, message='Your license plate state must be your state abbreviation'), Regexp('^(?-i:A[LKSZRAEP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$', message='Your license plate state must be your state abbreviation')])
    #license_no = StringField("License Number", validators = [InputRequired(message='You must enter your license number')])
    #license_plate_no = StringField("License Plate Number", validators = [InputRequired(message='You must enter your license plate number')])
    plate_state = SelectField("State", choices = [('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'), ('GU', 'GU'), ('PR', 'PR'), ('VI', 'VI')], default = 'NC')
    submit = SubmitField("Submit") 

class SearchFormFactory(FlaskForm):
    ride_no = IntegerField("Ride #", validators=[Optional()])
    origin_city = SelectField("Origin City:", coerce=str, choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PA', 'Philadelphia, PA'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')], default = 'Durham, NC')
    #destination = SelectField("Destination City:", validators = [InputRequired(message='Please enter destination'), NotEqualTo('origin_city')], choices = [('Search All', 'Search All'), ('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PA', 'Philadelphia, PA'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')])
    destination = SelectField("Destination City:", validators = [InputRequired(message='Please enter destination')], choices = [('Search All', 'Search All'), ('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PA', 'Philadelphia, PA'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')])
    #date = DateField("Departure Date:", validators=[InputRequired(message='Please enter desired departure date'), DateRange(min = datetime.date.today())], format='%Y-%m-%d')
    date = DateField("Departure Date:", validators=[InputRequired(message='Please enter desired departure date')], format='%Y-%m-%d')
    # earliest_departure = TimeField("Earliest Time of Departure:", validators=[InputRequired(message='Please enter the earliest time of departure')], format='%H:%M')
    # latest_departure = TimeField("Latest Time of Departure:", validators=[InputRequired(message='Please enter the latest time of departure'), GreaterThan('earliest_departure')], format='%H:%M')
    spots_needed = IntegerField("Spots Needed:", validators=[InputRequired(message='Please enter spots needed')], default=1)
    submit = SubmitField("Search")
                                        
class ListRideFormFactory(FlaskForm):
    # current_date = DateField('Current Date', default=datetime.date.today(), format='%Y-%m-%d', validators = [DataRequired()])
    #destination = SelectField("Destination City:", validators = [InputRequired(message='You must select a destination city'), NotEqualTo('origin_city')], choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PA', 'Philadelphia, PA'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')], )
    destination = SelectField("Destination City:", validators = [InputRequired(message='You must select a destination city'), NotEqualTo('origin_city')], choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PA', 'Philadelphia, PA'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')])
    origin_city = SelectField("Origin City:", coerce=str, choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PA', 'Philadelphia, PA'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonio, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')], default = 'Durham, NC')
    #driver_netid = StringField("Driver NetID:", validators = [InputRequired(message='You must enter your driver netID'), Length(min=4, max=7, message='Your NetID must be between 4 to 7 characters')])
    # date = DateField("Departure Date:", validators=[InputRequired(message='Please enter departure date'), GreaterThan('current_date')], format='%Y-%m-%d')
    date = DateField("Departure Date:", validators=[InputRequired(message='Please enter desired departure date'), DateRange(min = datetime.date.today())], format='%Y-%m-%d',)
    earliest_departure = TimeField("Earliest Time of Departure:", validators=[InputRequired(message='Please enter the earliest time of departure')], format='%H:%M')
    latest_departure = TimeField("Latest Time of Departure:", validators=[InputRequired(message='Please enter the latest time of departure'), GreaterThan('earliest_departure')], format='%H:%M')
    seats_available = IntegerField("Number of Seats Available:", validators = [InputRequired(message='You must enter the number of seats available')])
    gas_price = DecimalField("Gas Price:", places=2, rounding=None, validators=[Optional(), NumberRange(min=0, message='Gas price must be a positive number.')])
    comments = StringField("Comments:")
    submit = SubmitField("Submit")

class EditInfoFactory(FlaskForm):
    phone_number = IntegerField("Phone Number:") # validators = [Length(min=7, max=10, message='not long enough')])- do later
    #affiliation = SelectField("Affiliation:", choices = [('Graduate', 'Graduate'), ('Undergraduate', 'Undergraduate')])
    #school = SelectField("School:", choices = [('Pratt', 'Pratt'), ('Trinity', 'Trinity'), ('Fuqua', 'Fuqua'), ('Law', 'Law'), ('Medicine', 'Medicine'), ('Nicholas', 'Nicholas'), ('Nursing', 'Nursing'), ('Other', 'Other')])
    #license_plate_no = StringField("License Plate Number", validators = [Length(min=2, max=10, message='You must enter a license plate number between 2 to 10 characters')])
    license_plate_no = StringField("License Plate Number")
    plate_state = SelectField("State", choices = [('No Change', 'No Change'), ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'), ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'), ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'), ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'), ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'), ('GU', 'GU'), ('PR', 'PR'), ('VI', 'VI')], default = 'No Change')
    currentPassword = PasswordField("Current password needed to make changes", validators = [InputRequired(message='Must enter password to confirm changes')])
    password = PasswordField("New password:") # validators = [Length(min=5, max=100, message='Your password must be at least 5 characters and no more than 100')])
    confirmPassword = PasswordField("Confirm Password:", validators = [EqualTo('password')]) 
    #password = PasswordField("New password or enter current password to make changes:", validators = [InputRequired(message='Must enter password to make changes')])
    #confirmPassword = PasswordField("Confirm Password:", validators = [InputRequired(message='Must confirm password')])
    submit = SubmitField("Save")

class RideNumberFactory(FlaskForm):
    ride_no = IntegerField("Ride number of ride you would like to edit:", validators = [InputRequired(message='You must enter a ride number')])
    submit = SubmitField("Enter")

class RideNetIdNumberFactory(FlaskForm):
    ride_no = IntegerField("Ride number of ride you would like to search:", validators = [InputRequired(message='You must enter a ride number')])
    submit = SubmitField("Enter")    

class EditRideFactory(FlaskForm):
    #date = DateField("Departure Date:",  format='%Y-%m-%d', validators=[DateRange(min = datetime.date.today())])
    #earliest_departure = TimeField("Earliest Time of Departure:", validators = [Optional()], format='%H:%M:%S')
    #latest_departure = TimeField("Latest Time of Departure:", validators = [Optional()], format='%H:%M:%S')  #validators=[GreaterThan('earliest_departure')],
    #seats_available = IntegerField("Number of Seats Available:")
    gas_price = DecimalField("Gas Price:", places=2, rounding=None, validators=[NumberRange(min=0, message='Gas price must be a positive number.')])
    comments = StringField("Comments:", validators=[Optional()])
    cancel = SelectField("Would you like to cancel this ride?", choices = [('No', 'No'), ('Yes', 'Yes')])
    submit = SubmitField("Save")

class EditReservationFactory(FlaskForm):
    spots_needed = IntegerField("Spots Needed:", validators = [InputRequired(message='You must enter spots needed')])
    cancel = SelectField("Would you like to cancel your reservation for this ride?", choices = [('No', 'No'), ('Yes', 'Yes')])
    submit = SubmitField("Save")

class ReserveRideFormFactory(FlaskForm):
    rideNumber = HiddenField("Ride #", id="input-rideno")
    spots_needed = IntegerField("Spots Needed:", validators = [InputRequired(message='You must enter the number of seats needed')])
    notes = StringField("Notes:", validators=[Optional()])
    submit = SubmitField("Request Ride")

class EditRideTimeFactory(FlaskForm):
    #earliest_departure = TimeField("Earliest Time of Departure:", validators = [InputRequired(message=' ')], format='%H:%M')
    #latest_departure = TimeField("Latest Time of Departure:", validators = [InputRequired(message='You must enter the latest time of departure'), GreaterThan('earliest_departure')], format='%H:%M')
    #latest_departure = TimeField("Latest Time of Departure:", validators = [InputRequired(message=' '), GreaterThan('earliest_departure')], format='%H:%M')
    
    earliest_departure = TimeField("Earliest Time of Departure:", validators=[InputRequired(message=' ')], format='%H:%M')
    latest_departure = TimeField("Latest Time of Departure:", validators=[InputRequired(message=' '), GreaterThan('earliest_departure')], format='%H:%M')
 
    submit = SubmitField("Save")