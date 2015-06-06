#!/usr/bin/env bash

#Step-0 Create a properly configured AWS Linux

#Step-1:From AWS Linux VM initial creation, to install evrything necessary to run a django project

###############################################################################
# Purpose: one script install, config, django, posgres, gunicorn, nginx,
# Todo: Virtualenv environment
# Todo: Refactor, Centos/Redhat
#
###############################################################################

# User Variables (edit these)
DJANGO_PROJECT_NAME='myproject' # name of your django project
POSTGRES_DB_NAME='mydb' # name of the database that your django project will use

# BEGIN SCRIPT

# don't run this as root
WHOAMI=`whoami`
if [ "${WHOAMI,,}" == "root" ]; then
	echo "Don't run this script with sudo or as root."
	exit
fi

# output script echos to stderr
echoerr() { echo "$@" 1>&2; }

# clean up and trapping functions
cleanup() {
  rm -f /home/$WHOAMI/django/
  sudo rm /etc/nginx/sites-enabled/*
  sudo rm /etc/nginx/sites-available/$DJANGO_PROJECT_NAME
  return $?
}

control_c() {
  echoerr "Ctrl+c pressed. Exiting... ***\n"
  cleanup
  exit $?
}

# trap keyboard interrupt (control-c)
trap control_c SIGINT

# activate sudo for this session
if [ 1 -eq 1 ] # sudo echoerr "This script needs sudo access..."; then
then
	echoerr "Access Granted. Genesis starting..."
else
	exit
fi

# Step One: Update Packages
echoerr "Step One: Update Packages"

sudo yum update
sudo yum -y install gcc*  # gcc is needed by psycopg2 etc
sudo yum upgrade

sudo yum install python-pip
sudo pip install --upgrade pip
sudo ln -sf /usr/local/bin/pip /usr/bin/pip

# Step Two: Install and Create Virtualenv
echoerr "Step Two: Install and Create Virtualenv (not implemented)"

# Skipped... this script is for new machines

# Step Three: Install Django
echoerr "Step Three: Install Django"
sudo pip install django

# Step Four: Install PostgreSQL
echoerr "Step Four: Install PostgreSQL"
sudo yum -y install python27-devel.x86_64

sudo yum -y install postgresql93*

sudo  /etc/init.d/postgresql93 initdb
sudo chkconfig  postgresql93 on
sudo  /etc/init.d/postgresql93 start

# Step Five: Install NGINX
echoerr "Step Five: Install NGINX"
sudo yum install nginx

# Step Six: Install Gunicorn
echoerr "Step Six: Install Gunicorn"
sudo pip install gunicorn

# Step Seven: Configure PostgreSQL
printf "postgres\npostgres" | sudo passwd postgres

echoerr "Step Seven: Configure PostgreSQL"
echoerr "Password is \"postgres\" (no quotes)"

#create a database with postgres as the user

#create user $WHOAMI psycopg2

sudo su postgres -c "createuser  $WHOAMI"

#alter database mydb owner to ubuntu;
sudo su postgres -c "createdb \"$POSTGRES_DB_NAME\" -O  $WHOAMI"

#until su postgres -c "createdb \"$POSTGRES_DB_NAME\" -O ubuntu;" # no need to create new role
#do
#	echoerr "Wrong password. Password is \"postgres\" (no quotes). Try again"
#done

# Step Eight: Create a Django Project
echoerr "Step Eight: Create a Django Project"

mkdir /home/$WHOAMI/django/
cd /home/$WHOAMI/django/


django-admin.py startproject $DJANGO_PROJECT_NAME

sudo pip install psycopg2

cd /home/$WHOAMI/django/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME
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

cd /home/$WHOAMI/django/$DJANGO_PROJECT_NAME/

#python manage.py syncdb
python manage.py migrate
retval=$?

if [ $retval -ne 0 ]; then
echoerr " Failed db migration !"
else
echoerr " create a superuser"
# Not again  python manage.py createsuperuser
fi

# Step Nine: Configure Gunicorn
echoerr "Step Nine: Configure Gunicorn"

echo "command = '/usr/local/bin/gunicorn'
pythonpath = '/home/$WHOAMI/django/$DJANGO_PROJECT_NAME'
bind = '127.0.0.1:8001'
workers = 1" > /home/$WHOAMI/django/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME/gunicorn_config.py
# workers = 3" > /home/$WHOAMI/django/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME/gunicorn_config.py

# Step Ten: Configure NGINX
echoerr "Step Ten: Configure NGINX"

mkdir /home/$WHOAMI/django/static/

sudo cp -r /usr/local/lib/python2.7/site-packages/django/contrib/admin/static/admin/ /home/$WHOAMI/django/static/

sudo echo "
server {
	server_name localhost;
	access_log off;
	location /static/admin/ {
		alias /home/$WHOAMI/django/static/admin/;
	}
	location /static/ {
		alias /home/$WHOAMI/django/static/;
	}
	location / {
			proxy_pass http://127.0.0.1:8001;
			proxy_set_header X-Forwarded-Host \$server_name;
			proxy_set_header X-Real-IP \$remote_addr;
			add_header P3P 'CP=\"ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV\"';
	}
}" > /home/$WHOAMI/$DJANGO_PROJECT_NAME

sudo mv /home/$WHOAMI/$DJANGO_PROJECT_NAME /etc/nginx/sites-available

sudo ln -s /etc/nginx/sites-available/$DJANGO_PROJECT_NAME /etc/nginx/sites-enabled/$DJANGO_PROJECT_NAME

sudo rm /etc/nginx/sites-enabled/default

sudo service nginx restart

# Start the server
echoerr "Starting django..."

cd /home/$WHOAMI/django/$DJANGO_PROJECT_NAME/
gunicorn -c $DJANGO_PROJECT_NAME/gunicorn_config.py $DJANGO_PROJECT_NAME.wsgi &

echoerr "
Django is now running in the background.
Navigate to http://localhost/ to make sure that Django is working.
"

# FIN
