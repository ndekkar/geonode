DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': 'geonode',
         'USER': 'geonode',
         'PASSWORD': 'geonode',
     },
    # vector datastore for uploads
    'datastore' : {
        #'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'ENGINE': '', # Empty ENGINE name disables 
        'NAME': 'geonode',
        'USER' : 'geonode',
        'PASSWORD' : 'geonode',
        'HOST' : 'localhost',
        'PORT' : '5432',
    }
}

# OGC (WMS/WFS/WCS) Server Settings
OGC_SERVER = {
    'default' : {
        'BACKEND' : 'geonode.geoserver',
        'LOCATION' : 'http://localhost:8080/geoserver/',
        'USER' : 'admin',
        'PASSWORD' : 'geoserver',
        'MAPFISH_PRINT_ENABLED' : True,
        'PRINTNG_ENABLED' : True,
        'GEONODE_SECURITY_ENABLED' : True,
        'GEOGIT_ENABLED' : False,
        'WMST_ENABLED' : False,
        # Set to name of database in DATABASES dictionary to enable
        'DATASTORE': '', #'datastore',
    }
}