#!/bin/bash
/home/junaid/.local/bin/gunicorn --access-logfile /home/junaid/logs/pothole/gunicorn-access.log --error-logfile /home/junaid/logs/pothole/gunicorn-error.log wsgi