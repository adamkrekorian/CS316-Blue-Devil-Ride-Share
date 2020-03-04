
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('home.html')

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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug = True)