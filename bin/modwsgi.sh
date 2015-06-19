#! /bin/sh
#
# /etc/init.d/modwsgi.sh
#
# chkconfig: 345 95 05
# description: modwsgi daemon service
#
# fei.zhang@ga.gov.au
# Geoscience Australia
#
# Provides: modwsgi and httpd for django
# Required-Start: $local_fs $network
# Required-Stop: $local_fs $network
# Should-Start:  345
# Should-Stop: 0 1 6
### END INIT INFO

############################################################
# 2015-06-15
# This is a stub script to be installed in /etc/init.d to provide service
# config: /opt/django/myproject/modwsgi-p8888
# SeeAlso
# http://www.tldp.org/HOWTO/HighQuality-Apps-HOWTO/boot.html
# http://serverfault.com/questions/29788/what-is-needed-for-a-linux-service-to-be-supported-by-chkconfig
#
# to call the control sacript below
# USAGE: /etc/init.d/modwsgi.sh start/stop|status
#------------------------------------------------------------
# Source function library, is this really needed?
# . /etc/rc.d/init.d/functions


# Call up a self-contained django python app in
PATH2CMD=/opt/django/myproject/modwsgi-p8888/apachectl
$PATH2CMD  $@
