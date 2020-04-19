
from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from sqlalchemy import distinct, update
from datetime import date
from database import db
import pdb

#app = Flask(__name__)
#app.secret_key = 's3cr3t' #change this?
#app.config.from_object('config')

#db = SQLAlchemy(app, session_options={'autocommit': False})

import forms
import models

#Grace's variables
rideToEdit = None

bp = Blueprint('rides', __name__, url_prefix = '/rides', template_folder = 'templates')

@bp.route('/')
def home_page():
    if 'driver' in session:
        print(session['driver'])
    return render_template('home.html')# are going to have to set some values here equal to something like in beers- to return values?

@bp.route('/find-rides', methods=('GET', 'POST'))
def find_rides():
    form = forms.SearchFormFactory()
    reserveForm = forms.ReserveRideFormFactory()

    if 'logged_in' not in session:
        if session['logged_in']==False:
            flash("You are not logged in. Redirecting you to log in.")
            return redirect(url_for('rides.log_in'))

    if 'logged_in' in session and session['logged_in']==False:
        flash("You are not logged in. Redirecting you to log in.")
        return redirect(url_for('rides.log_in'))     

    else:
        if form.validate_on_submit():

            origin_city = request.form['origin_city']
            destination = request.form['destination']
            date = request.form['date']
            spots_needed = request.form['spots_needed']

            if destination == "Search All":
                results = db.session.query(models.Ride) \
                    .filter(models.Ride.origin == origin_city) \
                    .filter(models.Ride.date == date) \
                    .filter(models.Ride.seats_available >= spots_needed).all()

            else:
                results = db.session.query(models.Ride) \
                    .filter(models.Ride.origin == origin_city) \
                    .filter(models.Ride.destination == destination) \
                    .filter(models.Ride.date == date) \
                    .filter(models.Ride.seats_available >= spots_needed).all()
            results = [x.__dict__ for x in results]
            print('we are hereeeeeeee')
            return render_template('find-rides.html', form=form, reserveForm = reserveForm, results = results)
    
    print(reserveForm.validate_on_submit())
    print(reserveForm.errors)
    #note- I changed this to be request.form because it works for me
    
    if reserveForm.validate_on_submit():
        rideno = int(request.form['rideNumber'])
        spots_needed = int(request.form['spots_needed'])
        notes = request.form['notes']

        #update seats available in ride
        edit_ride = db.session.query(models.Ride).filter(models.Ride.ride_no == rideno).one()
        print(edit_ride.seats_available - spots_needed)
        edit_ride.seats_available = edit_ride.seats_available - spots_needed
        db.session.commit()

        #create entry in Reserve
        newEntry = models.Reserve(rider_netid = session['netid'], ride_no = rideno, seats_needed = spots_needed, note = notes)
        db.session.add(newEntry)
        db.session.commit()

    return render_template('find-rides.html', form=form, reserveForm = reserveForm)


@bp.route('/list-rides', methods=['GET','POST'])
def list_rides():
    form = forms.ListRideFormFactory()
    driver = models.Driver.query.filter_by(netid=session['netid']).first()
    if 'logged_in' in session and not driver:
        if session['logged_in']:
            flash("You are signed in but not yet a driver. Redirecting you to driver registration.") #These flash messages aren't displaying on the site
            return redirect(url_for('rides.register_driver', form=forms.RegisterDriverFormFactory()))
    if 'logged_in' not in session:
        if session['logged_in']==False:
            flash("You are not logged in. Redirecting you to log in.")
            return redirect(url_for('rides.log_in'))
    if 'logged_in' in session and session['logged_in']==False:
        flash("You are not logged in. Redirecting you to log in.")
        return redirect(url_for('rides.log_in'))     
    else:
        print(form.errors)

        if form.is_submitted():
            print("submitted")

        if form.validate():
            print("valid")
        

        print(form.errors)
        if form.validate_on_submit():
            driver_netid = request.form['driver_netid']
            destination = request.form['destination']
            origin_city = request.form['origin_city']
            date = request.form['date']
            earliest_departure = request.form['earliest_departure']
            latest_departure = request.form['latest_departure']
            seats_available = request.form['seats_available']
            gas_price = request.form['gas_price']
            if gas_price == '':
                gas_price = None
            comments = request.form['comments']
            if comments=='':
                comments = None
            session['driver'] = True
            newride = models.Ride(driver_netid=driver_netid, destination=destination, origin=origin_city, date=date, earliest_time=earliest_departure, latest_time=latest_departure, seats_available=seats_available, gas_price=gas_price, comments=comments)
            db.session.add(newride)
            db.session.commit()

            return redirect(url_for('rides.home_page'))
    return render_template('list-rides.html', form=form)

@bp.route('/sign-up', methods=['GET','POST'])
def sign_up():
    form = forms.RegisterFormFactory()
    #if 'driver' in session:
    #    driver = models.Driver.query.filter_by(netid=session['netid']).first()
    #if 'logged_in' in session and 'driver' in session:
    #    if session['logged_in'] == True and session['driver']==False:
    #        flash("You are signed in but not yet a driver. Redirecting you to driver registration.") #These flash messages aren't displaying on the site
    #        return redirect(url_for('rides.register_driver', form=forms.RegisterDriverFormFactory()))
    #if 'logged_in' in session and 'driver' in session:
    #    if session['logged_in'] and session['driver']:
    #        flash("You are signed in and already registered as a driver. Redirecting you to list a ride.")
    #        return redirect(url_for('rides.list_rides'))
    #else:
        
        #print(form.errors)

        #if form.is_submitted():
            #print("submitted")

        #if form.validate():
            #print("valid")

        #print(form.errors)
    if form.validate_on_submit():
        netid = request.form['netid']
        name = request.form['name']
        duke_email = request.form['duke_email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        affiliation = request.form['affiliation_sel']
        school = request.form['school']

        register = models.Rideshare_user(netid=netid, name=name, duke_email=duke_email, phone_number=phone_number, password=password, affiliation=affiliation, school=school)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for('rides.log_in'))
        #return render_template('sign-up.html', form=form)
    return render_template('sign-up.html', form=form)

@bp.route('/register-driver', methods=['GET','POST'])
def register_driver():
    form = forms.RegisterDriverFormFactory()
    driver = models.Driver.query.filter_by(netid=session['netid']).first()
    if 'logged_in' in session and driver:
        if session['logged_in']:
            flash("You are already a driver. Redirecting you to list a ride.")
        return redirect(url_for('rides.list_rides'))
    print(form.errors)

    if form.is_submitted():
        print("submitted")

    if form.validate():
        print("valid")

    print(form.errors)
    if form.validate_on_submit():
        netid = session['netid']
        license_no = request.form['license_no']
        license_plate_no = request.form['license_plate_no']
        plate_state = request.form['plate_state']
        register = models.Driver(netid=netid, license_no=license_no, license_plate_no=license_plate_no, plate_state=plate_state)
        session['driver'] = True
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('rides.list_rides'))
    return render_template('register-driver.html', form=form)
    

@bp.route('/log-in', methods=['GET','POST'])
def log_in():
    error = None
    if request.method == 'POST':
        netid = request.form.get('netid')
        password = request.form.get('password')
        user = models.Rideshare_user.query.filter_by(netid=netid).first()
        if not user or not (user.password==password):
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            session['netid'] = netid
            driver = models.Driver.query.filter_by(netid=session['netid']).first()
            if not driver:
                session['driver'] = False
            else:
                session['driver'] = True
            return redirect(url_for('rides.home_page'))
    return render_template('log-in.html', error=error)

@bp.route("/logout")
def log_out():
    session['logged_in'] = False
    session['netid'] = None
    session['driver'] = False
    return home_page()

@bp.route('/account', methods=('GET', 'POST'))
def account():
    
    user = models.Rideshare_user.query.filter_by(netid=session['netid']).first()
    ridesListed = models.Ride.query.filter_by(driver_netid=session['netid']).order_by(models.Ride.ride_no.desc())
    ridesReservedTemp = models.Reserve.query.filter_by(rider_netid=session['netid']).order_by(models.Reserve.ride_no.desc())
    ridesReserved = []

    for ride in ridesReservedTemp:
        ridesReserved.append(models.Ride.query.filter_by(ride_no=ride.ride_no).first())

    #ridesReservedFinal = ridesReserved.order_by(models.Ride.date.desc())
    #SORT rides listed and rides reserved by date- really hard


    driver = models.Driver.query.filter_by(netid=session['netid']).first()
    if ridesListed.first()==None:
        ridesListed = None
    if ridesReserved == []:
        ridesReserved = None

    return render_template('account.html', user=user, driver=driver, ridesListed=ridesListed, ridesReserved=ridesReserved)

@bp.route('/edit-info', methods=('GET', 'POST'))
def editInfo():
    user = models.Rideshare_user.query.filter_by(netid=session['netid']).first()
    form = forms.EditInfoFactory()

    
    
    #print("errors: ")
    #print(form.errors)
    #if form.is_submitted():
        #print("submitted")

    #if form.validate():
        #print("valid")


    if form.validate_on_submit():
        netid=user.netid
        name=user.name
        duke_email=user.duke_email
        phone_number=request.form['phone_number']
        #note should I update so they can choose affiliation and school?
        affiliation=user.affiliation
        school=user.school
        #dont need to check if equal to confirm because form does that for me
        password=request.form['password']

        newUser = models.Rideshare_user(netid=netid, name=name, duke_email=duke_email, phone_number=phone_number, affiliation= affiliation, school=school, password=password)
        # ERROR WITH WRONG SESSION
        #db.session.delete(userInfo)
        #db.session.add(newUser)
        #db.session.commit()
        print("NEW PASS next try")
        print(request.form['password'])
        #user.password = request.form['password']
        #user.phone_number = request.form['phone_number']
        #user.password = "gracel"
        #user.update()
        print("="*50)
        flash("User information updated.")
        return redirect(url_for('rides.account'))
    
    return render_template('edit-info.html', user=user, debug=True, form=form)
    
@bp.route('/edit-list-ride', methods=('GET', 'POST'))
def editRides():
    form = forms.EditRideFactory()
    formRideNo = forms.RideNumberFactory()
    #cancelForm = forms.CancelRideFactory()
    validRideNo = False
    ride = None
    
    
    if formRideNo.validate_on_submit():
        rideNumber = request.form['ride_no']
        global rideToEdit
        rideToEdit = db.session.query(models.Ride) \
                    .filter(models.Ride.ride_no == rideNumber) \
                    .filter(models.Ride.driver_netid == session['netid']).first()
        ride = rideToEdit
        if (ride == None):
            flash("Ride not found.")
            return redirect(url_for('rides.account'))
        else: 
            print(ride.earliest_time)
            validRideNo = True

    
    print("FORM ERRORS")
    print(form.errors)
    #pdb.set_trace()
    if form.is_submitted():
        print("FORM submitted")

    if form.validate():
        print("FORM valid")

    if form.validate_on_submit():
        print(rideToEdit.comments)
        #edit ride form here- rideToEdit is a global variable representing the ride you are editing
        reservesAffected = models.Reserve.query.filter_by(ride_no=rideToEdit.ride_no)
        netIDsAffected = None

        for reservation in reservesAffected:
            netIDsAffected.append(reservation.rider_netid)

        #could I check net ids affected with??
        if (netIDsAffected != None):
            for netidAffected in netIDsAffected:
                session['netidAffected']
                flash("One of your reserved rides has changed")

        #print(netIDsAffected.first())
        
        cancel = request.form['cancel']
        print("TEST1 checking if cancelling")
        print(cancel == "Yes")
        if cancel == "Yes":
            #how to delete a ride?
            db.session.delete(rideToEdit)
            db.session.commit()
            print("ride cancelled")
            flash("Ride cancelled.")
        else:
            #update ride here- bunch of if statements to see if null- if no changes set usersAffected to null
            date = request.form['date']
            earliest_departure = request.form['earliest_departure']
            latest_departure = request.form['latest_departure']
            seats_available = request.form['seats_available']
            gas_price = request.form['gas_price']
            comments = request.form['comments']
            #db.session.update(ride)
            #db.session.commit()


            #how to check if empty correctly?
            #if date == None:
                #date = ride.date
            #if earliest_departure == None:
                #earliest_departure = ride.earliest_departure
            #if latest_departure == None:
                #latest_departure = ride.latest_departure
            #if seats_available == None:
                #seats_available = ride.seats_available
            #if gas_price == None:
                #gas_price = ride.gas_price
            #if comments == None:
                #comments = ride.comments


            flash("Ride updated.")
        return redirect(url_for('rides.account'))

    #if cancelForm.validate_on_submit():
        #how to delete here? recreate object?
        #print("ride cancelled")
        #flash("Ride cancelled.")
        #return redirect(url_for('rides.account'))


    return render_template('edit-list-ride.html', form=form, formRideNo=formRideNo, validRideNo = validRideNo, ride=ride)

#@bp.route('/edit-ride', methods=('GET', 'POST'))
#def editRidesInformation():
    #form=forms.EditRideFactory()

    #if form.validate_on_submit():
        #print("form worked")
        #update ride information here

    #return render_template('edit-ride.html', debug=True, form=form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
