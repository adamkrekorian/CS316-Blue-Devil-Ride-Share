#!/bin/bash
gunicorn --bind 0.0.0.0:8080 "duke_ride_share:create_app()"