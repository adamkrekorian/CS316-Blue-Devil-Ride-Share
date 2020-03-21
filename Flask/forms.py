from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, validators, DateField, SubmitField, SelectField, ValidationError
from wtforms_components import TimeField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from app import db
import models
import datetime

class RegisterFormFactory(FlaskForm):
    netid = StringField("NetID:", validators = [DataRequired(), Length(min=4, max=7)], message=("You must enter your NetID"))
    name = StringField("Name:", validators = [DataRequired(), Length(min=5, max=256)], message=("You must enter your name"))
    duke_email = StringField("Duke Email:", validators = [DataRequired(), Email(), Length(min=10, max=256), Regexp('^[a-zA-Z0-9]+@duke.edu$')], message=("You must enter a valid Duke email"))
    phone_number = IntegerField("Phone Number:", validators = [DataRequired()], message=("You must enter your phone number"))
    password = PasswordField("Password:", validators = [DataRequired(), Length(min=5, max=256)], message=("You must enter a password"))
    affiliation_sel = SelectField("Affiliation:", validators = [DataRequired()], choices = [('Graduate', 'Graduate'), ('Undergraduate', 'Undergraduate')], message=("You must select your affiliation"))
    school = SelectField("School:", validators = [DataRequired()], choices = [('Pratt', 'Pratt'), ('Trinity', 'Trinity'), ('Fuqua', 'Fuqua'), ('Law', 'Law'), ('Medicine', 'Medicine'), ('Nicolas', 'Nicolas'), ('Nursing', 'Nursing'), ('Other', 'Other')], message=("You must enter your affiliation"))
    submit = SubmitField("Submit")      

class RegisterDriverFormFactory(FlaskForm):
    license_no = StringField("License Number", validators = [DataRequired(), Length(min=5, max=50)], message=("You must enter your license number"))
    license_plate_no = StringField("License Plate Number", validators = [DataRequired(), Length(min=2, max=8)], message=("You must enter your license plate number"))
    plate_state = StringField("State", validators = [DataRequired(), Length(min=2, max=2), Regexp('^(?-i:A[LKSZRAEP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$')], message=("You must enter the state of your license plate (i.e. NC)"))
    submit = SubmitField("Submit")

class SearchFormFactory(FlaskForm):
    start_city = SelectField("Start City", validators = [DataRequired()], message=("You must select an origin"))
    end_city = SelectField("Destination") #may need coerce=unicode for this and line above
    #need to add date picker
    #need to add start time picker
    #need to add end time picker
    spots_needed = IntegerField("Spots Needed")
    submit = SubmitField("Search")

class ListRideFormFactory(FlaskForm):
    origin = SelectField("Affiliation:", validators = [DataRequired()], choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PN', 'Philadelphia, PN'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonia, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')], validators = [DataRequired()])
    destination = SelectField("Affiliation:", validators = [DataRequired()], choices = [('Albuquerque, NM', 'Albuquerque, NM'), ('Arlington, TX', 'Arlington, TX'), ('Asheville, NC', 'Asheville, NC'), ('Aspen, CO', 'Aspen, CO'), ('Atlanta, GA', 'Atlanta, GA'), ('Austin, TX', 'Austin, TX'), ('Baltimore, MD', 'Baltimore, MD'), ('Boca Grande, FL', 'Boca Grande, FL'), ('Boston, MA', 'Boston, MA'), ('Cary, NC', 'Cary, NC'), ('Charlotte, NC', 'Charlotte, NC'), ('Chicago, IL', 'Chicago, IL'), ('Colorado Springs, CO', 'Colorado Springs, CO'), ('Columbus, OH', 'Columbus, OH'), ('Concord, NC', 'Concord, NC'), ('Dallas, TX', 'Dallas, TX'), ('Denver, CO', 'Denver, CO'), ('Detroit, MI', 'Detroit, MI'), ('Durham, NC', 'Durham, NC'), ('El Paso, TX', 'El Paso, TX'), ('Fayetteville, NC', 'Fayetteville, NC'), ('Fort Worth, TX', 'Fort Worth, TX'), ('Fresno, CA', 'Fresno, CA'), ('Greensboro, NC', 'Greensboro, NC'), ('Greenville, NC', 'Greenville, NC'), ('High Point, NC', 'High Point, NC'), ('Houston, TX', 'Houston, TX'), ('Indianapolis, IN', 'Indianapolis, IN'), ('Jacksonville, FL', 'Jacksonville, FL'), ('Kansas City, MO', 'Kansas City, MO'), ('Las Vegas, NV', 'Las Vegas, NV'), ('Long Beach, CA', 'Long Beach, CA'), ('Los Angeles, CA', 'Los Angeles, CA'), ('Louisville, KY', 'Louisville, KY'), ('Memphis, TN', 'Memphis, TN'), ('Mesa, AZ', 'Mesa, AZ'), ('Miami, FL', 'Miami, FL'), ('Milwaukee, WI', 'Milwaukee, WI'), ('Minneapolis, MN', 'Minneapolis, MN'), ('Myrtle Beach, SC', 'Myrtle Beach, SC'), ('Nashville, TN', 'Nashville, TN'), ('New Orleans, LA', 'New Orleans, LA'), ('New York, NY', 'New York, NY'), ('Oakland, CA', 'Oakland, CA'), ('Oklahoma City, OK', 'Oklahoma City, OK'), ('Omaha, NE', 'Omaha, NE'), ('Philadelphia, PN', 'Philadelphia, PN'), ('Phoenix, AZ', 'Phoenix, AZ'), ('Portland, OR', 'Portland, OR'), ('Raleigh, NC', 'Raleigh, NC'), ('Sacramento, CA', 'Sacramento, CA'), ('San Antonio, TX', 'San Antonia, TX'), ('San Diego, CA', 'San Diego, CA'), ('San Francisco, CA', 'San Francisco, CA'), ('San Jose, CA', 'San Jose, CA'), ('Seattle, WA', 'Seattle, WA'), ('Tucson, AZ', 'Tucson, AZ'), ('Tulsa, OK', 'Tulsa, OK'), ('Virginia Beach, VA', 'Virginia Beach, VA'), ('Washington, DC', 'Washington, DC'), ('Wichita, KS', 'Wichita, KS'), ('Wilmington, NC', 'Wilmington, NC'), ('Winston-Salem, NC', 'Winston-Salem, NC')], validators = [DataRequired()])
    driver_netid = StringField("Driver NetID:", validators = [DataRequired(), Length(min=4, max=7), message=("You must enter your NetID")])
    date = DateField('Departure Date', format='%m/%d/%Y', validators = [DataRequired()])
    earliest_time = TimeField('Earliest Departure Time', format='%H:%M:%S', validators = [DataRequired()])
    latest_time = TimeField('Latest Departure Time', format='%H:%M:%S', validators = [DataRequired()])
    seats_available = IntegerField("Number of Seats Available, validators = [DataRequired()]")
    #gas_price = 
    comments = StringField("Comments")
                                       