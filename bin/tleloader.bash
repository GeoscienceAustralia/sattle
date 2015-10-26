#!/bin/env bash
# make sure this file is executable chmod u+x
# Commandline Usage:
#  This_script path2/TLEfiles &>> /tmp/tle_loader.log

echo "Invoke python script to ingest TLE-files data into Target DB "

# which python verison to use (must have MySQLDb driver,...)
PYTHON_INTERPRETER=python2.7  #OR python2.7 or /usr/local/bin/python2.7

### tleserv project, can injest TLE data into MySQL (and Postgresql, if configured correctly)
#$PYTHON_INTERPRETER -m tle2db.tle_loader  "$@"

#-------------------------------------------------------
##Fei use django framework Postgres Database backend
# activaste virtualenv by source
source  /opt/django/PyVenv/bin/activate
export PYTHONPATH=/opt/django/sattle  #where is the project modules installed?
unset DJANGO_SETTINGS_MODULE #will use default one: settings.py
$PYTHON_INTERPRETER -m tleserv.tleclient.load_tle_into_db "$@"

#Use another settings file, not working becuase the satellite tables different columns
#export DJANGO_SETTINGS_MODULE="sattle.settings_mysql"
#$PYTHON_INTERPRETER -m tleserv.tleclient.load_tle_into_db "$@"