
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#copied this from h4- do we think we need?
app.secret_key = 's3cr3t' #probably going to have to change this
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})

@app.route('/')
def home_page():
    return render_template('home.html') # are going to have to set some values here equal to something like in beers- to return values?

@app.route('/find-rides')
def find_rides():
    return render_template('find-rides.html')

@app.route('/list-rides')
def list_rides():
    return render_template('list-rides.html')

@app.route('/sign-up')
def sign_up():
    return render_template('sign-up.html')

@app.route('/log-in')
def log_in():
    return render_template('log-in.html')

#can remove if wanted-just trying out
@app.route('/edit-list-ride')
def edit_list_ride(ride): #passes in an entire ride object
    form=forms.listRideForm.form(ride)
    return render_template('edit-list-ride.html', ride=ride, form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)