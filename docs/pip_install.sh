#!/bin/bash

# if use virtualenv
source ../PyVenv/bin/activate

#get proxy for http/https://outside.ga
source /etc/fetch.conf.d/proxy.sh
pip install --upgrade pip

# for psycopg2 to compile
# devel packages are commonly required for successful gcc compile.
export PATH=/usr/pgsql-9.4/bin:$PATH

pip install -r requirement.txt

echo "After installation "
echo "pip freeze to show the installed packages"
pip freeze


