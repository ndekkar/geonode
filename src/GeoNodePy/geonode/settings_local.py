
###########################################################
# SITE SPECIFIC SETTINGS
# Overriding generic settings - uncomment and edit to change
###########################################################

#SITE_ID = 1
#SITENAME = "GeoNode"
# Change to actual URL
#SITEURL = 'http://localhost:8000/'
#ROOT_URLCONF = 'geonode.urls'

# Add additional apps here (appended to INSTALLED_APPS)
#SITE_APPS = ()

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'myv-y4#7j-d*p-__@j#*3z@!y24fz8%^z2v6atuy4bo9vqr1_a'
#REGISTRATION_OPEN = False
#ACCOUNT_ACTIVATION_DAYS = 7

#ADMINS = ( ('Your Name', 'your_email@domain.com'),)

# Datastore settings to make geonode upload vector layers directly to postgis
#DB_DATASTORE=False
#DB_DATASTORE_NAME = ''
#DB_DATASTORE_DATABASE = '' #DATABASE_NAME
#DB_DATASTORE_USER = '' #DATABASE_USER
#DB_DATASTORE_PASSWORD = '' #DATABASE_PASSWORD
#DB_DATASTORE_HOST = ''
#DB_DATASTORE_PORT = ''
#DB_DATASTORE_TYPE='postgis'

# Local time zone for this installation. http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment set to same as your system time zone.
#TIME_ZONE = 'America/New_York'

# Language code for this installation.
#LANGUAGE_CODE = 'en'

# ASSETS_ROOT is only used on production servers when using collectstatic command
# it is where all the static and media files are served from
#ASSETS_ROOT = '/var/www/geonode/'
# URL to static web server that serves CSS, uploaded media, javascript, etc.
# for serving from same server or in development, use '/'
#ASSETS_URL = '/'

# Google API key if using Google maps
#GOOGLE_API_KEY = "ABQIAAAAkofooZxTfcCv9Wi3zzGTVxTnme5EwnLVtEDGnh-lFVzRJhbdQhQgAhB1eT_2muZtc0dl-ZSWrtzmrw"

###########################################################
# MODE SPECIFIC SETTINGS
# These settings assume a development environment.
# For production, override these in settings_local
###########################################################

DEVELOPMENT = True

# General Debug mode. Sometimes useful to turn on in Production
DEBUG = DEVELOPMENT
# Template debugging
TEMPLATE_DEBUG = DEBUG
# This tells the development server to serve static files
SERVE_MEDIA = DEVELOPMENT

# This is a useful 3rd party django app, install separately
DEBUG_TOOLBAR = False
# If installed, useful to link it to DEBUG setting
# DEBUG_TOOLBAR = DEBUG

if DEVELOPMENT is True:
    SITEURL = 'http://localhost:8000/'
else:
    # Change to real production database
    DATABASES = {
          # Example postgres DB
          'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'geonode',
                'USER': 'geonode',
                'PASSWORD': 'password',
                'HOST': 'localhost',
                'PORT': '5432',
            }
        }
    # Uncomment the following to use a Gmail account as the email backend
    #EMAIL_USE_TLS = True
    #EMAIL_HOST = 'smtp.gmail.com'
    #EMAIL_HOST_USER = 'email'
    #EMAIL_HOST_PASSWORD = 'pw'
    #EMAIL_PORT = 587
