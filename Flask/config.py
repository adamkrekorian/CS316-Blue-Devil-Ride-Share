import os

SQLALCHEMY_DATABASE_URI = "postgresql://rideshare:{}@vcm-13365.vm.duke.edu/production".format(os.environ['DBPASSWORD'])
SQLALCHEMY_ECHO = True
DEBUG = True