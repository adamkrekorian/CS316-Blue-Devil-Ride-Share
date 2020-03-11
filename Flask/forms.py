from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, IntegerField, PasswordField, validators

from wtforms import StringField, BooleanField, SelectField, SubmitField, PasswordField
from wtforms import validators, ValidationError
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from app import db
import models

class RegisterFormFactory(FlaskForm):
    netid = StringField("NetID:", validators = [DataRequired(), Length(min=4, max=7)])
    name = StringField("Name:", validators = [DataRequired(), Length(min=5, max=256)])
    duke_email = StringField("Duke Email:", validators = [DataRequired(), Length(min=10, max=256), Regexp('^[a-zA-Z0-9]+@duke.edu$')])
    phone_number = IntegerField("Phone Number:", validators = [DataRequired()])
    password = PasswordField("Password:", validators = [DataRequired(), Length(min=5, max=256)])
    affiliation_sel = SelectField("Affiliation:", validators = [DataRequired()], choices = [('Graduate', 'Graduate'), ('Undergraduate', 'Undergraduate')])
    school = SelectField("School:", validators = [DataRequired()], choices = [('Pratt', 'Pratt'), ('Trinity', 'Trinity'), ('Fuqua', 'Fuqua'), ('Law', 'Law'), ('Medicine', 'Medicine'), ('Nicolas', 'Nicolas'), ('Nursing', 'Nursing'), ('Other', 'Other')])
    submit = SubmitField("Submit")      

class RegisterDriverFormFactory(FlaskForm):
    license_no = StringField("License Number", validators = [DataRequired(), Length(min=5, max=50)])
    license_plate_no = StringField("License Plate Number", validators = [DataRequired(), Length(min=2, max=8)])
    plate_state = StringField("State", validators = [DataRequired(), Length(min=2, max=2), Regexp('^(?-i:A[LKSZRAEP]|C[AOT]|D[EC]|F[LM]|G[AU]|HI|I[ADLN]|K[SY]|LA|M[ADEHINOPST]|N[CDEHJMVY]|O[HKR]|P[ARW]|RI|S[CD]|T[NX]|UT|V[AIT]|W[AIVY])$')])
    submit = SubmitField("Submit")
    

                                       