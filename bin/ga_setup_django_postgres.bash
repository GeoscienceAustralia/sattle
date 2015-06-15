#!/usr/bin/env bash
###############################################################################
# Purpose:  One cmd script to install, config, django, postgres, gunicorn, nginx, modwsgi
#           Python Virtualenv environment, all pyhton package installed by pip into PyVenv
#
# Author: fei.zhang@ga.gov.au
# Date: 2015-06-02
# Usage: Redhat-CentOS in GA
# edit the first few lines according to your VM IP then run it as a non-root user, who has sudo privilege
#
# Todo: Deploy a real App.
# Todo: Puppert/Ansible/Docker
# Todo: Further modulize and refactor
###############################################################################

FqdnameOrIpAddress='10.10.19.44'  # edit this according to your VM's FQDN or IP

PROJECTS_DIR=/opt/django  #where the djangos projects will be created

DJANGO_PROJECT_NAME='myproject' # name of your django project

POSTGRES_DB_NAME='mydb' # name of the database that your django project will use

PYTHON_VENV_NAME='PyVenv'

##--------------------------------------------------------------------------------
# nothing needs to be changed below this line
##--------------------------------------------------------------------------------
# BEGIN SCRIPT

WHOAMI=`whoami`  # unix user: fzhang

sudo mkdir -p $PROJECTS_DIR

sudo chown -R ${WHOAMI} $PROJECTS_DIR

ls -l $PROJECTS_DIR
# exit

if [ "${WHOAMI}" == "root" ]; then
        echo "Don't run this script as root."
        exit
fi

# output
myprint() { echo "$@" 1>&2; }

control_c() {
  myprint "Ctrl+c pressed. Exiting... ***\n"
  cleanup
  exit $?
}

# Install and Configure PostgreSQL
setup_postgres() {

    #  Install PostgreSQL93 or 94
    sudo yum -y install postgresql94*

    sudo  /etc/init.d/postgresql-9.4 initdb
    sudo chkconfig  postgresql-9.4 on
    sudo  /etc/init.d/postgresql-9.4 start

    #create user $WHOAMI
    sudo su postgres -c "createuser  $WHOAMI"

    #alter database mydb owner to ubuntu;
    sudo su postgres -c "createdb \"$POSTGRES_DB_NAME\" -O  $WHOAMI"

}

setup_django(){

    virtualenv $PROJECTS_DIR/$PYTHON_VENV_NAME
    source $PROJECTS_DIR/$PYTHON_VENV_NAME/bin/activate

    myprint "pip Install Django and DB drivers"
    #sudo
    pip install django

    export PATH=/usr/pgsql-9.4/bin:$PATH   ## GA specific for pg_config to install psycopg2
    pip install psycopg2

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


    cd $PROJECTS_DIR/$DJANGO_PROJECT_NAME
    python manage.py migrate
    retval=$?

    if [ $retval -ne 0 ]; then
        myprint " Failed db migration !"
    else
    myprint " create a superuser"
    # Not again
        python manage.py createsuperuser
    fi
 }

# Install Gunicorn
setup_gunicorn(){
    myprint "Install Gunicorn"

    virtualenv $PROJECTS_DIR/$PYTHON_VENV_NAME
    source $PROJECTS_DIR/$PYTHON_VENV_NAME/bin/activate

    #sudo
    pip install gunicorn

    # Configure Gunicorn
    myprint "Configure Gunicorn"

    echo "
command = '/usr/local/bin/gunicorn'
pythonpath = '$PROJECTS_DIR/$DJANGO_PROJECT_NAME'
bind = '$FqdnameOrIpAddress:8001'  #OR  '0.0.0.0:8001'
workers = 1
# user = 'nobody'
    " > $PROJECTS_DIR/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME/gunicorn_config.py
    # workers = 3" > $PROJECTS_DIR/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME/gunicorn_config.py

    # Start the server
    myprint "Starting gunicorn django..."

    cd $PROJECTS_DIR/$DJANGO_PROJECT_NAME/

    # to run the gunicorn (as nobody user) sudo gunicorn
    gunicorn -c $DJANGO_PROJECT_NAME/gunicorn_config.py $DJANGO_PROJECT_NAME.wsgi &

   echo "Testing at:  http://$FqdnameOrIpAddress/admin "
}

setup_nginx() {

    #Install NGINX
    myprint "Install NGINX"
    sudo yum -y install nginx

    myprint " Configure NGINX"

    mkdir $PROJECTS_DIR/static/

    #this may fail for virtualenv
    sudo cp -r /usr/local/lib/python2.7/site-packages/django/contrib/admin/static/admin/ $PROJECTS_DIR/static/

    sudo echo "
    server {
        server_name localhost;
        access_log off;
        location /static/admin/ {
            alias $PROJECTS_DIR/static/admin/;
        }
        location /static/ {
            alias $PROJECTS_DIR/static/;
        }
        location / {
                proxy_pass http://127.0.0.1:8001;
                proxy_set_header X-Forwarded-Host \$server_name;
                proxy_set_header X-Real-IP \$remote_addr;
                add_header P3P 'CP=\"ALL DSP COR PSAa PSDa OUR NOR ONL UNI COM NAV\"';
        }
    }" >  /etc/nginx/sites-available/$DJANGO_PROJECT_NAME

    sudo ln -s /etc/nginx/sites-available/$DJANGO_PROJECT_NAME /etc/nginx/sites-enabled/$DJANGO_PROJECT_NAME

    sudo rm /etc/nginx/sites-enabled/default

    sudo service nginx restart

}

setup_modwsgi(){

MOD_WSIG_USER=$WHOAMI  #beaware this run user might be used to connect postgres db (see setting.py)
MOD_WSIG_GROUP=$WHOAMI
#libs required by modwsgi
sudo yum install httpd.x86_64
sudo yum install httpd-devel.x86_64

virtualenv $PROJECTS_DIR/$PYTHON_VENV_NAME
source $PROJECTS_DIR/$PYTHON_VENV_NAME/bin/activate
pip install mod-wsgi

# massage the setting.py to use mod-wsgi server
    cd $PROJECTS_DIR/$DJANGO_PROJECT_NAME/$DJANGO_PROJECT_NAME

    SETTINGS_PY=`cat settings.py`

    TARGET="'django.contrib.staticfiles',"
    NEW_STUFF="'django.contrib.staticfiles', 'mod_wsgi.server',";

    SETTINGS_PY="${SETTINGS_PY/$TARGET/$NEW_STUFF}"

    echo "$SETTINGS_PY" > settings.py
    echo "STATIC_ROOT = '$PROJECTS_DIR/static/'" >> settings.py

    cd  $PROJECTS_DIR/$DJANGO_PROJECT_NAME
    python manage.py collectstatic

$PROJECTS_DIR/$PYTHON_VENV_NAME/bin/python  manage.py runmodwsgi --setup-only --port=8888 --user $MOD_WSIG_USER --group $MOD_WSIG_GROUP --server-root=./modwsgi-p8888

echo "please check and edit  modwsgi-p8888/apachectl"

}
#In the Beginning, .....
############################################################################
# trap keyboard interrupt (control-c)
trap control_c SIGINT

# activate sudo for this session
sudo -v  #validate
if [ $? -eq 0 ] # sudo myprint "This script needs sudo access..."; then
then
        echo "sudo access validated ......."
else
    echo "sudo problem: make sure the running user has sudo privilege"
        exit 1
fi

myprint "Update and install Packages"

sudo yum clean all  # clean cache

sudo yum -y update
sudo yum -y install gcc*  # gcc is needed by psycopg2 etc
sudo yum -y upgrade
sudo yum -y install python27-devel.x86_64
sudo yum -y install python-pip
sudo pip install --upgrade pip
#GA sudo yum -y install python27-pip.x86_64
sudo ln -sf /usr/local/bin/pip /usr/bin/pip

# Install and Create Virtualenv

sudo yum -y install python27-virtualenv.x86_64
sudo yum -y install python27-virtualenv.noarch

# call shell functions
setup_postgres

setup_django

#setup_gunicorn
#setup_nginx

#OR mod-wsgi
setup_modwsgi

##################################################################################################################

