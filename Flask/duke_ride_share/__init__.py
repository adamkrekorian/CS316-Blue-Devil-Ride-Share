import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dukebluedevil')
    app.config.from_object('config')
    db = SQLAlchemy(app, session_options={'autocommit': False})
    with app.app_context():
        from controllers import rides
        app.register_blueprint(rides.bp)    
    return app
