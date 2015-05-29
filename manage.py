#!/usr/bin/env python
#  python2.7 with django* installed
#  To test run the Web server
#  ./manage.py runserver 0.0.0.0:8000

import os
import sys

if __name__ == "__main__":
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sattle.settings")
    # More specifically
    os.environ["DJANGO_SETTINGS_MODULE"] = "sattle.settings"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
