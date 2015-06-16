#! /bin/sh
#
# /etc/init.d/modwsgi.sh
#
# chkconfig: 345 95 05
# description: modwsgi daemon service
#
# processname: modwsgi
# config: /opt/django/myproject/modwsgi-p8888
# SeeAlso
# http://www.tldp.org/HOWTO/HighQuality-Apps-HOWTO/boot.html
# http://serverfault.com/questions/29788/what-is-needed-for-a-linux-service-to-be-supported-by-chkconfig
#
# Example:
# [fzhang@pe-master init.d]$ vi modwsgi.sh
# A stub script to be installed in /etc/init.d to provide service
# fei.zhang@ga.gov.au
# 2015-06-15

# to call the control sacript below
# USAGE: /etc/init.d/modwsgi-p8888 start/stop|status
# chkconfig --add -list --del  name
# chkconfig modwsgi.sh on
#------------------------------------------------------------
# Source function library. Is this neessary
. /etc/rc.d/init.d/functions


# Call up a self-contained django python app in
PATH2CMD=/opt/django/myproject/modwsgi-p8888/apachectl
$PATH2CMD  $@
