"""
Django settings for sattle project.

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gcm673f%o+bl7p&djg*k(#!v1tyy#*x+$(m0qly+1420&n*)$9'

# SECURITY WARNING: don't run with debug in production!
#DEBUG = True   #for dev env
DEBUG = False   #for prod env

#ALLOWED_HOSTS = []      #for dev env
ALLOWED_HOSTS = [ '*',] #for prod env



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'rest_framework.authtoken',
    'tleserv',
    'mod_wsgi.server',  #have this before runmodwsgi See  https://pypi.python.org/pypi/mod_wsgi
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'sattle.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 'loaders': [
            #     # insert your TEMPLATE_LOADERS here
            #     ('django.template.loaders.filesystem.Loader',
            #     'django.template.loaders.app_directories.Loader')
            # ],
        },
    },
]

WSGI_APPLICATION = 'sattle.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
# googles: django how to non-default db
# https://docs.djangoproject.com/en/1.8/topics/db/multi-db/

# see doc about using non-default databases (Manually selecting a database)
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # },
    'default-dev0': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sattle',
    },
    # postgresql connection credential. need config in production
    'default':{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rmsdb',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
         },
    #mysql
    'default-mysql':{
        'ENGINE': 'django.db.backends.mysql', 
        'OPTIONS': { 'read_default_file': '~/etc/mysql.cnf', },
        }

}

## Local customisation in yaml file  (or environ setting)
import yaml
with open('/etc/fetch.conf.d/dbconf.yaml', 'r') as f: mydbs = yaml.load(f)
# get the db credential accoding to the config yaml file
Postgres = mydbs['postgresdb']

#override the db
DATABASES['default']['HOST'] = Postgres['host']
DATABASES['default']['NAME'] = Postgres['dbname']
DATABASES['default']['USER'] = Postgres['user']
DATABASES['default']['PASSWORD'] = Postgres['password']

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = '/var/www/django/sattle/static/'   #then run python2.7 manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')   #then run python2.7 manage.py collectstatic
