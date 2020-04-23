
from flask import Flask, render_template, redirect, url_for, request, session, flash, Blueprint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from sqlalchemy import distinct, update, create_engine
from datetime import date
from database import db
import pdb
import os
from sqlalchemy.orm import sessionmaker

#graces imports
import datetime

#prepared statements
#engine = create_engine('postgresql://rideshare:{}@vcm-13365.vm.duke.edu/production'.format(os.environ['DBPASSWORD']))
#conn = engine.connect()

#search prepared statements
#db.session.execute('''PREPARE SearchAll (varchar, date, integer) AS SELECT * FROM Ride WHERE origin = $1 AND date = $2 and seats_available >= $3;''')
#db.session.execute('''PREPARE Search (varchar, varchar, date, integer) AS SELECT * FROM Ride WHERE origin = $1 AND destination = $2 AND date = $3 and seats_available >= $4;''')
#list prepared statements -- doesnt work
#db.session.execute('''PREPARE List (varchar, varchar, varchar, date, time, time, integer, integer, varchar) AS INSERT INTO Ride VALUES (DEFAULT, $1, $2, $3, $4, $5, $6, $7, $8, $9);''')
#account prepared statements
#db.session.execute('''PREPARE RidesPosted (varchar) AS SELECT * FROM Ride WHERE driver_netid = $1 ORDER BY date DESC;''')
#db.session.execute('''PREPARE Reservations (varchar) AS SELECT * FROM Reserve R1, Ride R2 WHERE R1.rider_netid = $1 AND R1.ride_no = R2.ride_no ORDER BY date DESC;''')
#db.session.commit()
#app = Flask(__name__)
#app.secret_key = 's3cr3t' #change this?
#app.config.from_object('config')

#db = SQLAlchemy(app, session_options={'autocommit': False})

import forms
import models

#Grace's global variables
rideToEdit = None
reservationToEdit = None
rideToEditTime = None

bp = Blueprint('rides', __name__, url_prefix = '/rides', template_folder = 'templates')

@bp.route('/')
def home_page():
    if 'driver' in session:
        print(session['driver'])
    return render_template('home.html')# are going to have to set some values here equal to something like in beers- to return values?

@bp.route('/find-rides', methods=('GET', 'POST'))
def find_rides():
    form = forms.SearchFormFactory()
    #errors = [] cant redirect after using- need to return template
    results = []
    reserveForm = forms.ReserveRideFormFactory() #should remove
    print("in find rides")
    print("="*20)
    readyToReserve = False

    if 'logged_in' not in session:
        if session['logged_in']==False:
            flash("You are not logged in. Redirecting you to log in.")
            return redirect(url_for('rides.log_in'))

    if 'logged_in' in session and session['logged_in']==False:
        flash("You are not logged in. Redirecting you to log in.")
        return redirect(url_for('rides.log_in'))     

    else:
        if form.validate_on_submit():
            print("find form valid and submitted")
            origin_city = request.form['origin_city']
            destination = request.form['destination']
            date = request.form['date']
            spots_needed = request.form['spots_needed']

            print("data gathered")
            print("="*50)
            print(origin_city)
            print(destination)
            print(date)
            print(spots_needed)

            if origin_city == destination:
                print("HEREEEE WHERE ORIGIN AND DESTINATION EQUAL")
                #errors.append("Origin and destination cannot be the same.") #not printing
                flash("Origin and destination cannot be the same.")
                return redirect(url_for('rides.find_rides'))

            if date < str(datetime.date.today()):
                flash("Date entered must be after today's date.")
                return redirect(url_for('rides.find_rides'))

            resultsTemp = None
            if destination == "Search All":
                resultsTemp = db.session.query(models.Ride)\
                    .filter(models.Ride.origin == origin_city)\
                    .filter(models.Ride.date == date)\
                    .filter(models.Ride.seats_available >= spots_needed)
                #resultsTemp = db.session.execute('EXECUTE SearchAll(:origin_city, :date, :spots_needed)',\
                    #{"origin_city":origin_city, "date":date, "spots_needed":spots_needed})
            else:
                resultsTemp = db.session.query(models.Ride)\
                    .filter(models.Ride.origin == origin_city)\
                    .filter(models.Ride.destination == destination)\
                    .filter(models.Ride.date == date)\
                    .filter(models.Ride.seats_available >= spots_needed)
                #resultsTemp = db.session.execute('EXECUTE SearchAll(:origin_city, :date, :spots_needed)',\
                    #{"origin_city":origin_city, "destination":destination, "date":date, "spots_needed":spots_needed})
            myRides = db.session.query(models.Ride).filter(models.Ride.driver_netid == session['netid'])
            myRidesNumbers = []
            #could be simplified 
            for ride in myRides:
                myRidesNumbers.append(ride.ride_no)
            for ride in resultsTemp:
                if not (ride.ride_no in myRidesNumbers):
                    results.append(ride)
                    print(ride)

            print("PRINTING RESULTS")
            for result in results:
                print(result.ride_no)
            print("DONE PRINTING RESULTS")
                
            results = [x.__dict__ for x in results] #what does this do?
            #print('we are hereeeeeeee')
            #print("and here's what is in errors")
            #print(errors[0])
            #print("that's what was in errors")
            return render_template('find-rides.html', form=form, reserveForm=reserveForm, results=results, readyToReserve=readyToReserve)
        #technically don't need if form always validating on submit
        return render_template('find-rides.html', form=form, reserveForm = reserveForm, results = results) 

#RETURN RENDER TEMPLATE
@bp.route('/reserve-rides', methods=('GET', 'POST'))      
def reserveRide():
    print("in reserve rides")
    print("="*20)
    reserveForm = forms.ReserveRideFormFactory()
    form = forms.SearchFormFactory()
    #errors = [] add into return statement too

    if reserveForm.validate_on_submit():
        print("reserve form valid and submit")
        rideno = int(request.form['rideNumber'])
        spots_needed = int(request.form['spots_needed'])
        notes = request.form['notes']
       
        edit_ride = db.session.query(models.Ride).filter(models.Ride.ride_no == rideno).one()
        #dont allow to book ride if requesting more spots than there is available
        if spots_needed > edit_ride.seats_available:
            flash("Not enough spots in this ride as you changed spots needed from your initial request.")
            return redirect(url_for('rides.find_rides'))
            #errors.append("Not enough spots in this ride as you changed spots needed from your initial request.")- ideal
            #return render_template('find-rides.html', form=form, reserveForm = reserveForm, errors=errors)

        #dont allow to book ride if they already have booked the same ride
        previousReservationTemp = None
        previousReservationTemp = db.session.query(models.Reserve).filter(models.Reserve.ride_no == rideno).filter(models.Reserve.rider_netid == session['netid']).first()
        if previousReservationTemp != None:
            flash("You have already reserved this ride. Please edit your number of spots in the account page.")
            return redirect(url_for('rides.find_rides')) 
        print(edit_ride.seats_available - spots_needed) 

        #update seats available in ride
        edit_ride.seats_available = edit_ride.seats_available - spots_needed
        db.session.commit()

        #create entry in Reserve
        newEntry = models.Reserve(rider_netid = session['netid'], ride_no = rideno, seats_needed = spots_needed, note = notes)
        db.session.add(newEntry)
        db.session.commit()
        flash("Successfully booked.")
    print("end of find rides")
    return render_template('find-rides.html', form=form, reserveForm = reserveForm)


@bp.route('/list-rides', methods=['GET','POST'])
def list_rides():
    form = forms.ListRideFormFactory()
    driver = models.Driver.query.filter_by(netid=session['netid']).first()   

    if form.validate_on_submit():
        driver_netid = session['netid']
        destination = request.form['destination']
        origin_city = request.form['origin_city']
        date = request.form['date']
        #could simplify this with a where statement 
        myRides = db.session.query(models.Ride).filter(models.Ride.driver_netid == session['netid'])
        for ride in myRides:
            if str(date) == str(ride.date):
                flash("You already are driving a ride on this day.")
                return redirect(url_for('rides.list_rides'))
        #should have join here like prepared statement in accounts- get list of reservations with date then do:
        #myReservations = ?? prepared statement
        #for ride in myReservations:
            #if date == ride.date:
                #flash("You already have a reservation on this day.")
                #return redirect(url_for('rides.list_rides'))

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
        #newride = db.session.execute('EXECUTE List(:origin_city, :destination, :driver_netid, :date, :earliest_departure, :latest_departure, :seats_available, :gas_price, :comments)',\
                #{"origin_city":origin_city, "destination":destination, "driver_netid":driver_netid, "date":date, "earliest_departure":earliest_departure, "latest_departure":latest_departure, "seats_available":seats_available, "gas_price":gas_price, "comments":comments})
        newride = models.Ride(driver_netid=driver_netid, destination=destination, origin=origin_city, date=date, earliest_time=earliest_departure, latest_time=latest_departure, seats_available=seats_available, gas_price=gas_price, comments=comments)
        db.session.add(newride)
        db.session.commit()
        flash("Ride successfully listed.")
        return redirect(url_for('rides.list_rides'))
    return render_template('list-rides.html', form=form)

@bp.route('/sign-up', methods=['GET','POST'])
def sign_up():
    form = forms.RegisterFormFactory()

    if form.validate_on_submit():
        netid = request.form['netid']
        name = request.form['name']
        duke_email = request.form['duke_email']
        phone_number = request.form['phone_number']
        password = request.form['password']
        affiliation = request.form['affiliation_sel']
        school = request.form['school']

        if len(str(phone_number))<6 or len(str(phone_number))>10:
            flash("Your phone number must be at least 6 characters and no more than 10.")
            return redirect(url_for('rides.sign_up'))
        existingUsers = db.session.query(models.Rideshare_user).filter(models.Rideshare_user.netid == netid)
        if existingUsers.first() != None:
            flash("An account with this netid already exists. Please log in.")
            return redirect(url_for('rides.log_in'))

        register = models.Rideshare_user(netid=netid, name=name, duke_email=duke_email, phone_number=phone_number, password=password, affiliation=affiliation, school=school)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for('rides.log_in'))
        #return render_template('sign-up.html', form=form)
    return render_template('sign-up.html', form=form)

@bp.route('/register-driver', methods=['GET','POST'])
def register_driver():
    form = forms.RegisterDriverFormFactory()
    driver = models.Driver.query.filter_by(netid=session['netid']).first() #dont need
    #should never happen
    if 'logged_in' in session and driver:
        if session['logged_in']:
            flash("You are already a driver. Redirecting you to list a ride.")
        return redirect(url_for('rides.list_rides'))


    print(form.errors)
    if form.validate_on_submit():
        netid = session['netid']
        license_no = request.form['license_no']
        license_plate_no = request.form['license_plate_no']
        plate_state = request.form['plate_state']

        register = models.Driver(netid=netid, license_no=license_no, license_plate_no=license_plate_no, plate_state=plate_state)
        session['driver'] = True # what does this do?
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
    ridesListed = models.Ride.query.filter_by(driver_netid=session['netid']).order_by(models.Ride.date.desc())
    # ridesL = db.session.execute('EXECUTE RidesPosted(:driver_netid)', {"driver_netid":session['netid']})

    # ridesListed = []
    # row = ridesL.fetchone()
    # ridesListed.append(row)
    # while row is not None:
    #     row = ridesL.fetchone()
    #     ridesListed.append(row)
    
    # res = db.session.execute('EXECUTE Reservations(:driver_netid)', {"driver_netid":session['netid']})

    # reservations = []
    # row = res.fetchone()
    # reservations.append(row)
    # while row is not None:
    #     row = res.fetchone()
    #     reservations.append(row)

    #ridesReservedTemp = models.Reserve.query.filter_by(rider_netid=session['netid']).order_by(models.Reserve.ride_no.desc())
    #reservations = models.Reserve.query.join(models.Ride).filter_by(models.Reserve.ride_no=models.Ride.ride_no).filter_by(models.Reserve.rider_netid=session['netid'])
    #reservationsTemp = models.Ride.query.join(models.Ride.ride_no == models.Reserve.ride_no)
    reservations = db.session.query(models.Reserve).join(models.Ride).add_columns(models.Ride.comments, models.Ride.origin, models.Ride.date, models.Ride.destination, models.Ride.driver_netid, models.Ride.earliest_time, models.Ride.latest_time, models.Ride.seats_available, models.Ride.gas_price, models.Reserve.rider_netid, models.Reserve.ride_no, models.Reserve.note, models.Reserve.seats_needed).filter(models.Reserve.rider_netid == session['netid']).order_by(models.Ride.date.desc())
    #reservations = []

    #for ride in reservationsTemp:
    #    if ride.rider_netid == session['netid']:
    #        reservations.append(ride)

    #userList = users.query.join(friendships, users.id==friendships.user_id).add_columns(users.userId, users.name, users.email, friends.userId, friendId)\
    #.filter(users.id == friendships.friend_id).filter(friendships.user_id == userID)\
    #ridesReserved = []
    #for ride in ridesReservedTemp:
        #ridesReserved.append(models.Ride.query.filter_by(ride_no=ride.ride_no).first()) 
    #ridesReservedFinal = ridesReserved.order_by(models.Ride.date.desc())
    #SORT rides listed and rides reserved by date- really hard

    driver = models.Driver.query.filter_by(netid=session['netid']).first()
    if ridesListed.first()==None:
        ridesListed = None
    if reservations.first() == None:
        reservations = None

    return render_template('account.html', user=user, driver=driver, ridesListed=ridesListed, reservations=reservations)

@bp.route('/edit-info', methods=('GET', 'POST'))
def editInfo():
    user = models.Rideshare_user.query.filter_by(netid=session['netid']).first()
    form = forms.EditInfoFactory()
    print("HEREEE")
    driver = models.Driver.query.filter_by(netid=session['netid']).first()
    print("HEREEE2")
    if form.validate_on_submit():
        print("form validated")
        newphone_number=request.form['phone_number']
        #note should I update so they can choose affiliation and school?
        #newaffiliation=request.form['affiliation']
        #newschool=request.form['school']
        #dont need to check if equal to confirm because form does that for me
        if driver !=None:
            plateNum = request.form['license_plate_no']
            plateState = request.form['plate_state']
        else:
            plateNum=None
            plateState=None
        currentpassword = request.form['currentPassword']
        newpassword=request.form['password']
        confirmpassword = request.form['confirmPassword']
        print("starting ifs")
        #should be validator when phone number is a string
        if len(str(newphone_number))<6 or len(str(newphone_number))>10:
            flash("Your phone number must be at least 6 characters and no more than 10.")
            return redirect(url_for('rides.editInfo'))
        if plateNum!=None and (len(plateNum)<2 or len(plateNum)>10):
            flash("Your plate number must be at least 2 characters and no more than 10.")
            return redirect(url_for('rides.editInfo'))
        #if platenum is null and driver
        
        if currentpassword != user.password:
            flash("Password doesn't match current password. Changes could not be made.")
            return redirect(url_for('rides.editInfo'))
        
        print("ending ifs")
        user_edit = db.session.query(models.Rideshare_user).filter(models.Rideshare_user.netid == session['netid']).one()
        driver_edit = db.session.query(models.Driver).filter(models.Driver.netid == session['netid']).first()
        print("="*30)
        print(driver_edit == None)
        #if new password field wasn't empty then new password is equal to confirm password- only update password in this case
        if plateNum == None and driver_edit !=None:
            flash("Must enter plate number")
            return redirect(url_for('rides.editInfo'))
        if newpassword != '':
            print("new password is not null")
            if len(newpassword)<5 or len(newpassword)>100:
                flash("Your new password must be at least 5 characters and no more than 100")
                return redirect(url_for('rides.editInfo'))
            if newpassword != user.password:
                flash("Password updated.") 
            user_edit.password = newpassword
        #can just do this even if they do not make any changes
        user_edit.phone_number = newphone_number
        db.session.commit()
        
        if driver_edit == None:
            flash("User information updated.")
            return redirect(url_for('rides.account')) 

        driver_edit.license_plate_no = plateNum
        if plateState != 'No Change':
            driver_edit.plate_state = plateState
        db.session.commit()
        driver_edit.license_plate_no = plateNum
        if plateState != 'No Change':
            driver_edit.plate_state = plateState
        db.session.commit()
        #user_edit.affiliation = newaffiliation
        #user_edit.school = newschool
        
        flash("User information updated.")
        return redirect(url_for('rides.account'))

    
    return render_template('edit-info.html', user=user, debug=True, form=form, driver=driver)
    
@bp.route('/edit-list-ride-rideNo-Check', methods=('GET', 'POST'))
def editRidesRideNoCheck():
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

    return render_template('edit-list-ride.html', form=form, formRideNo=formRideNo, validRideNo = validRideNo, ride=ride)

@bp.route('/edit-list-ride', methods=('GET', 'POST'))
def editRides():
    form = forms.EditRideFactory()
    formRideNo = forms.RideNumberFactory()
    #cancelForm = forms.CancelRideFactory()
    validRideNo = True
    ride = None
    
    if form.validate_on_submit():
        ride = rideToEdit
        print(rideToEdit.comments)

        #figure out who the edits affect
        #reservesAffected = models.Reserve.query.filter_by(ride_no=rideToEdit.ride_no)
        #netIDsAffected = None
        #for reservation in reservesAffected:
            #netIDsAffected.append(reservation.rider_netid)
        #could I check net ids affected with??
        #ADD BACK IN LATER
        #if (netIDsAffected != None):
            #for netidAffected in netIDsAffected:
                #session['netidAffected']
                #flash("One of your reserved rides has changed")
        #print(netIDsAffected.first())

        rideNumber = rideToEdit.ride_no
        cancel = request.form['cancel']
        if cancel == "Yes":
            #how to delete a ride?
            reservationsToDelete = db.session.query(models.Reserve).filter(models.Reserve.ride_no == rideNumber)
            for reservation in reservationsToDelete:
                db.session.delete(reservation)
                db.session.commit()
            db.session.delete(rideToEdit)
            db.session.commit()
            print("ride cancelled")
            flash("Ride cancelled.")
        else:
           # newearliest_departure = request.form['earliest_departure']
            #newlatest_departure = request.form['latest_departure']
            newgas_price = request.form['gas_price']
            newcomments = request.form['comments']

            if newgas_price == '':
                newgas_price = None
            if newcomments=='':
                newcomments = None
            
            edit_ride = db.session.query(models.Ride).filter(models.Ride.ride_no == rideNumber).one()
            edit_ride.gas_price = newgas_price
            edit_ride.comments = newcomments
            #edit_ride.earliest_time = newearliest_departure
            #edit_ride.latest_time = newlatest_departure
            db.session.commit()
            flash("Ride updated.")

        return redirect(url_for('rides.account'))

    return render_template('edit-list-ride.html', form=form, formRideNo=formRideNo, validRideNo = validRideNo, ride=ride)


@bp.route('/edit-reservation', methods=('GET', 'POST'))
def editReservation():
    user = models.Rideshare_user.query.filter_by(netid=session['netid']).first()
    form = forms.EditReservationFactory()
    formRideNo = forms.RideNumberFactory()
    reservation = None
    validRideNo = False

    if formRideNo.validate_on_submit():
        rideNumber = request.form['ride_no']
        global reservationToEdit
        reservationToEdit = db.session.query(models.Reserve) \
                    .filter(models.Reserve.ride_no == rideNumber) \
                    .filter(models.Reserve.rider_netid == session['netid']).first()
        reservation = reservationToEdit
        if (reservation == None):
            flash("Reservation not found.")
            return redirect(url_for('rides.account'))
        else: 
            validRideNo = True

    if form.validate_on_submit():
        cancel = request.form['cancel']
        newSpots = 0
        rideNumber = reservationToEdit.ride_no
        ride = db.session.query(models.Ride) \
                    .filter(models.Ride.ride_no == rideNumber).first()

        if cancel == "Yes":
            #how to delete a ride?
            newSpots = reservationToEdit.seats_needed*-1
            print("PRINTING NEW SPOTS")
            print(newSpots)
            db.session.delete(reservationToEdit)
            db.session.commit()
            print("reservation cancelled")
            flash("Reservation cancelled.")
        #not cancelling-edit reservation
        else:
            updatedSpots = int(request.form['spots_needed'])
            print(updatedSpots)
            newSpots = updatedSpots - reservationToEdit.seats_needed
            print("NEW SPOTS")
            print(newSpots)
            print("AVAIL")
            print(ride.seats_available)
            if (updatedSpots > ride.seats_available):
                flash("Not enough room in the ride for spots needed. Reservation not updated.")
                return redirect(url_for('rides.account'))
            reservation_edit = db.session.query(models.Reserve).filter(models.Reserve.ride_no == rideNumber).filter(models.Reserve.rider_netid == session['netid']).first()
            reservation_edit.seats_needed = updatedSpots
            db.session.commit()
            flash("Reservation updated.")
        #edit seats available no matter what
        ride_edit = db.session.query(models.Ride).filter(models.Ride.ride_no == rideNumber).one()
        ride_edit.seats_available = ride.seats_available - newSpots
        db.session.commit()
        
        
        return redirect(url_for('rides.account'))
        #except BaseException as e:
            #form.errors['database'] = str(e) #could be wrong

        #return redirect(url_for('rides.account'))
    
    return render_template('edit-reservation.html', user=user, debug=True, form=form, validRideNo=validRideNo, formRideNo=formRideNo, reservation=reservation)

@bp.route('/riders-netids', methods=('GET', 'POST'))
def Riders_Netids():
    form = forms.RideNetIdNumberFactory()
    validRideNo = False
    ride = None
    reservations = None
    rideNumber = None
    
    if form.validate_on_submit():
        rideNumber = request.form['ride_no']
        ride = db.session.query(models.Ride).filter(models.Ride.ride_no == rideNumber).filter(models.Ride.driver_netid == session['netid']).first()
        if (ride == None):
            flash("Ride not found.")
            return redirect(url_for('rides.account'))
        else: 
            validRideNo = True
            reservations = db.session.query(models.Reserve).filter(models.Reserve.ride_no == ride.ride_no)
            if reservations.first() == None:
                reservations = None

    return render_template('riders-netids.html', form=form, validRideNo = validRideNo, reservations=reservations, rideNumber=rideNumber)

@bp.route('/edit-ride-time-rideNo-check', methods=('GET', 'POST'))
def editRideTimeRideNoCheck():
    form = forms.EditRideTimeFactory()
    formRideNo = forms.RideNumberFactory()
    validRideNo = False
    ride = None
    validatingRideNo = False

    print("in edit ride time ride no check")
    
    if formRideNo.validate_on_submit():
        print("ride check validated")
        validatingRideNo = True
        rideNumber = request.form['ride_no']
        global rideToEditTime
        rideToEditTime = db.session.query(models.Ride) \
                    .filter(models.Ride.ride_no == rideNumber) \
                    .filter(models.Ride.driver_netid == session['netid']).first()
        ride = rideToEditTime
        
        if (ride == None):
            flash("Ride not found.")
            return redirect(url_for('rides.account'))
        reservations = db.session.query(models.Reserve).filter(models.Reserve.ride_no == rideNumber)
        if reservations.first() == None:
            reservations = None
        if not (reservations == None): #check if people already reserved this
            flash("You cannot change the time of ride people have already reserved. Please coordinate with them directly. You can find their netids via the form on the right.")
            return redirect(url_for('rides.account')) 
        else:
            validRideNo = True
    print("leaving valid ride number project")
    print(validRideNo)

    return render_template('edit-ride-time.html', form=form, formRideNo=formRideNo, validRideNo = validRideNo, ride=ride)

@bp.route('/edit-ride-time', methods=('GET', 'POST'))
def editRideTimeRide():
    form = forms.EditRideTimeFactory()
    formRideNo = forms.RideNumberFactory()
    validRideNo = True
    ride = None
    print("in edit ride time ride")

    if form.validate_on_submit():
        ride = rideToEditTime
        rideNumber = rideToEditTime.ride_no
        newearliest_departure = request.form['earliest_departure']
        newlatest_departure = request.form['latest_departure']
        #if newlatest_departure < newearliest_departure:
           # flash("Must make latest time of depature after earliest time of departure. Changes not saved.")
            #return redirect(url_for('rides.editRideTimeRide'))
        edit_ride = db.session.query(models.Ride).filter(models.Ride.ride_no == rideNumber).one()
        edit_ride.earliest_time = newearliest_departure
        edit_ride.latest_time = newlatest_departure
        db.session.commit()
        flash("Ride time updated.")
        return redirect(url_for('rides.account'))

    return render_template('edit-ride-time.html', form=form, formRideNo=formRideNo, validRideNo = validRideNo, ride=ride)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)
