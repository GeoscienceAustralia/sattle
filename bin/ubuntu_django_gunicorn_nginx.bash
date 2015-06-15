#!/bin/bash
#
#Ref: https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn
###############################################################################
# Purpose:  One script install, config, django, postgres, gunicorn, nginx,
#           Python Virtualenv environment, all pyhton package installed by pip into myViPyEnv
#
# Author: fei.zhang@ga.gov.au
# Date: 2015-06-02
# Usage: edit the first few lines according to your VM IP then run it as a non-root user, who has sudo privilege
#
# Todo: Adop to other OS/apps.
# Todo: Puppert/Ansible/Docker
# Todo: can be further modulized and refactored
###############################################################################
# assume git has been installed so that this script can be pulled from github

# User Variables (edit these)
FqdnameOrIpAddress=128.199.190.92  #please edit this according to your VM's IP

PROJECTS_DIR=/opt/django2  #where the djangos projects will be created

DJANGO_PROJECT_NAME='myproject2' # name of your django project

POSTGRES_DB_NAME='mydb2' # name of the database that your django project will use

##--------------------------------------------------------------------------------
# nothing needs to be changed below this line
##--------------------------------------------------------------------------------

WHOAMI=`whoami`  # unix user: fzhang

sudo mkdir $PROJECTS_DIR

sudo chown ${WHOAMI} $PROJECTS_DIR

ls -l $PROJECTS_DIR
# exit

# BEGIN SCRIPT

# don't run this as root

if [ "${WHOAMI}" == "root" ]; then
	echo "Don't run this script with sudo or as root."
	exit
fi

# output script echos to stderr
echoerr() { echo "$@" 1>&2; }

# clean up and trapping functions
cleanup() {
  rm -f $PROJECTS_DIR/$DJANGO_PROJECT_NAME
  sudo rm /etc/nginx/sites-enabled/*
  sudo rm /etc/nginx/sites-available/$DJANGO_PROJECT_NAME
  return $?
}

control_c() {
  echoerr "Ctrl+c pressed. Exiting... ***\n"
  cleanup
  exit $?
}

config_setup_postgres() {

# Configure PostgreSQL
    printf "postgres\npostgres" | sudo passwd postgres

    echoerr "Configure PostgreSQL"
    echoerr "Password is \"postgres\" (no quotes)"

    #create a database with postgres as the user

    #create user $WHOAMI ubuntu

    sudo su postgres -c "createuser  $WHOAMI"

    #alter database mydb owner to ubuntu;
    sudo su postgres -c "createdb \"$POSTGRES_DB_NAME\" -O  $WHOAMI"

    #until su postgres -c "createdb \"$POSTGRES_DB_NAME\" -O ubuntu;" # no need to create new role
    #do
    #	echoerr "Wrong password. Password is \"postgres\" (no quotes). Try again"
    #done
}

# trap keyboard interrupt (control-c)
trap control_c SIGINT

# activate sudo for this session
# test if user has sudo priv

# Step One: Update Packages
echoerr "Step One: Update and install Packages"

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python-pip
sudo apt-get install python-virtualenv

# Step Four: Install PostgreSQL
echoerr "Install PostgreSQL"
sudo apt-get install libpq-dev python-dev
sudo apt-get install postgresql postgresql-contrib

# call shell function
config_setup_postgres

#  Install NGINX
echoerr "Install NGINX"
sudo apt-get install nginx

# Install and Create Virtualenv

virtualenv $PROJECTS_DIR/myViPyEnv
source $PROJECTS_DIR/myViPyEnv/bin/activate

# after activate the virtual python env, pip install below will done without sudo.
# Step Three: Install Django
echoerr "Step Three: Install Django"
 pip install django  #into myViPyEnv

# Step Six: Install Gunicorn
echoerr "Install Gunicorn"
pip install gunicorn #into myViPyEnv

# database driver
pip install psycopg2

# Create a Django Project
echoerr "Create a Django Project"

cd $PROJECTS_DIR/

django-admin.py startproject $DJANGO_PROJECT_NAME


cd $PROJECTS_DIR/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME
mv settings.py settings.py.backup # backup the original settings

SETTINGS_PY=`cat settings.py.backup`
TARGET="'ENGINE': 'django.db.backends.sqlite3'"
NEW_STUFF="'ENGINE': 'django.db.backends.postgresql_psycopg2'"

SETTINGS_PY="${SETTINGS_PY/$TARGET/$NEW_STUFF}"

NLT=$'\n\t'

TARGET="'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),"
#NEW_STUFF="'NAME': '$POSTGRES_DB_NAME',${NLT}'USER':'postgres',${NLT}'PASSWORD':'postgres',${NLT}'HOST':'',${NLT}'PORT':'',${NLT}";
NEW_STUFF="'NAME': '$POSTGRES_DB_NAME',${NLT}";


SETTINGS_PY="${SETTINGS_PY/$TARGET/$NEW_STUFF}"

echo "$SETTINGS_PY" > settings.py

cd $PROJECTS_DIR/$DJANGO_PROJECT_NAME/

#python manage.py syncdb
python manage.py migrate
retval=$?

if [ $retval -ne 0 ]; then
echoerr " Failed db migration !"
else
echoerr " create a superuser"
python manage.py createsuperuser
fi

# Step Nine: Configure Gunicorn
echoerr "Step Nine: Configure Gunicorn"

echo "command = '/usr/local/bin/gunicorn'
pythonpath = '$PROJECTS_DIR/$DJANGO_PROJECT_NAME'
bind = '$FqdnameOrIpAddress:8001'   #'127.0.0.1:8001'
workers = 1
#user = 'nobody'
" > $PROJECTS_DIR/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME/gunicorn_config.py
#? workers = 3" > $PROJECTS_DIR/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME/gunicorn_config.py

# Step Ten: Configure NGINX
echoerr "Step Ten: Configure NGINX"

mkdir $PROJECTS_DIR/static/

#this may fail for virtualenv
sudo cp -r /usr/local/lib/python2.7/dist-packages/django/contrib/admin/static/admin/ $PROJECTS_DIR/static/

sudo echo "
server {
	server_name $FqdnameOrIpAddress;
	access_log off;
	location /static/admin/ {
		alias $PROJECTS_DIR/static/admin/;
	}
	location /static/ {
		alias $PROJECTS_DIR/static/;
	}
	location / {
			proxy_pass http://$FqdnameOrIpAddress:8001;  #gunicorn
			proxy_set_header X-Forwarded-Host \$server_name;
			proxy_set_header X-Real-IP \$remote_addr;
			add_header P3P 'CP=\"ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV\"';
	}
}"  >    /tmp/$DJANGO_PROJECT_NAME

sudo cp /tmp/$DJANGO_PROJECT_NAME /etc/nginx/sites-available/$DJANGO_PROJECT_NAME

sudo ln -s /etc/nginx/sites-available/$DJANGO_PROJECT_NAME /etc/nginx/sites-enabled/$DJANGO_PROJECT_NAME

sudo rm /etc/nginx/sites-enabled/default

sudo service nginx restart

# Start the server
echoerr "Starting django..."

cd $PROJECTS_DIR/$DJANGO_PROJECT_NAME/

# to run the gunicorn (as nobody user) sudo gunicorn
gunicorn -c $DJANGO_PROJECT_NAME/gunicorn_config.py $DJANGO_PROJECT_NAME.wsgi &

echoerr "Django is now running in the background.    Navigate to http://$FqdnameOrIpAddress/admin to test"

# FIN