#! /bin/sh

# Ref [root@pe-master init.d]# cat modwsgi-p8888
# File: /etc/init.d/modwsgi.sh

# A stub script to be installed in /etc/init.d to provide service
# fei.zhang@ga.gov.au
# 2015-06-15

# to call the control sacript below
# USAGE: /etc/init.d/modwsgi-p8888 start/stop|status

# Call up a self-contained django python app in
PATH2CMD=/opt/django/myproject/modwsgi-p8888/apachectl
$PATH2CMD  $@
