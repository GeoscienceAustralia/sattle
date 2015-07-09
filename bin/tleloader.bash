#!/bin/env bash
# make sure this file is executable chmod u+x
# Commandline Usage:
#  This_script path2/TLEfiles &>> /tmp/tle_loader.log

echo "Invoke python script to ingest TLE-files data into Target DB "

# which python verison to use (must have MySQLDb driver,...)
PYTHON_INTERPRETER=python2.7  #OR python2.7 or /usr/local/bin/python2.7

### verison-1
#$PYTHON_INTERPRETER -m tle2db.tle_loader  "$@"

#-------------------------------------------------------
##Fei use django framework where is the project modules: /home/rms_usr/sattle
export PYTHONPATH=/opt/django/sattle
unset DJANGO_SETTINGS_MODULE #will use default one: settings.py
$PYTHON_INTERPRETER -m tleserv.tleclient.load_tle_into_db "$@"

#Use another settings file
export DJANGO_SETTINGS_MODULE="sattle.settings_mysql"
$PYTHON_INTERPRETER -m tleserv.tleclient.load_tle_into_db "$@"