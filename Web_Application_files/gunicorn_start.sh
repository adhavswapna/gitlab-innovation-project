#!/bin/bash

# This script starts Gunicorn with your Flask application

gunicorn -w 4 -b 0.0.0.0:5000 Web_Application_files.app:app

chmod +x gunicorn_start.sh
