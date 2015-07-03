#!/usr/bin/env bash

# This is a Django web application, not a usual python app.
# So, It will not be installed into the python site package as modules.

# It is strongly recommended to use python virtualenv to run the python application in a self-contianed manner.case
# It will enable complete isolate of the application from the system python installed packages.

#Pre-requesite  sudo yum python27 virtualenv and pip

##############################################################################################################
# where to install this Django webapp?
DjangoProjDirRoot=/opt/django

# get sattle package installed into $DjangoProjDirRoot
cd $DjangoProjDirRoot

# prepare the source as tar ball, the unpack here
# alternatively,
# git clone https://github.com/GeoscienceAustralia/sattle.git

cd sattle
# rm  -rf .git   #if want to forget the git repo

#---------------------------------
# create a virtual environment
virtualenv $DjangoProjDirRoot/PyVenv
#activate the virtualenv
source $DjangoProjDirRoot/PyVenv/bin/activate

#get proxy for http/https://outside.ga
source /etc/fetch.conf.d/proxy.sh
pip install --upgrade pip

# for psycopg2 to compile
# devel packages are commonly required for successful gcc compile.
export PATH=/usr/pgsql-9.4/bin:$PATH

pip install -r requirement.txt

echo "After installation "
echo "pip freeze to show the installed packages in the local virtualenv, compare with requirement.txt"
pip freeze

# double check sattle/setting.py for configuration modification

# static is part of the source code. do not need to run this again  ./manage.py  collectstatic

#./manage.py migrate  #This will connect to the default dataabse configured in the sattle/setting.py

#Just onece  ./manage.py createsuperuser # this will create a admin user for web UI login

#./manage.py runserver 0.0.0.0:8000   # this will start a http server at port 8000
#To see what command available ./manage.py help

# Assume RESTful http port=8888 for production
HTTP_PORT=8888

# Smoke testing using a web browser such as firefox, must open firewall, may need to configure browser LAN proxy
#http://IpAddress_Or_ServerHostName:$HTTP_PORT/sattle/admin/
#http://IpAddress_Or_ServerHostName:$HTTP_PORT/sattle/tleserv/


MODWSGIDIR=$DjangoProjDirRoot/sattle/modwsgi
$MODWSGIDIR/apachectl stop
# Now create modwsgi startup scripts and configuration for this Django app.
RUN_USER=rms_usr
RUN_GROUP=`id -gn $RUN_USER`

./manage.py runmodwsgi --setup-only --port=$HTTP_PORT --user $RUN_USER --group $RUN_GROUP --server-root=$MODWSGIDIR

# Beaware of dir/file permissions and fix if necessary, for example:
#(PyVenv)[fzhang@rhe-obsnet-prod02 sattle]$ chown -R fzhang:rms /home/fzhang
#(PyVenv)[fzhang@rhe-obsnet-prod02 sattle]$ chmod -R 750 /home/fzhang

cd $MODWSGIDIR

echo "Optional: Please edit the $MODWSGIDIR/apachectl to change the status command behavior as follows"
echo  replace the orginal line in status
echo  '		exec /opt/django/PyVenv/bin/python -m webbrowser -t $STATUSURL'
echo  by

echo   '	echo Check daemon process run by user  $MOD_WSGI_USER:'
echo   '	pgrep -u $MOD_WSGI_USER -lf $MOD_WSGI_SERVER_ROOT '




echo "Starting apache..."

./apachectl start

#./apachectl status
#./apachectl stop
#./apachectl status
#./apachectl start

# test the RESTFul API in browser:http://IpAddress_Or_ServerHostName:$HTTP_PORT/sattle/tleserv/
# test the Restful API in python clients: tleserv/telclient/*.py
