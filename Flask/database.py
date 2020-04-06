import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
