import os
import urlparse

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True'

TEMPLATE_DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['norrin.cngr.es']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'googleauth',
    'raven.contrib.django.raven_compat',
    'south',
    'norrin.appconfig',
    'norrin.notifications',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'norrin.context_processors.norrin_config',
)

ROOT_URLCONF = 'norrin.urls'

WSGI_APPLICATION = 'norrin.wsgi.application'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(),
}

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Man this is stuff.
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )


# authentication

GOOGLEAUTH_DOMAIN = 'sunlightfoundation.com'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'googleauth.backends.GoogleAuthBackend',
)


# Urban Airship

UA_KEY = os.environ.get('UA_KEY')
UA_SECRET = os.environ.get('UA_SECRET')
UA_MASTER = os.environ.get('UA_MASTER')


# MongoDB

MONGOHQ_URL = os.environ.get('MONGOHQ_URL', 'mongodb://localhost:27017/norrin')

o = urlparse.urlparse(MONGOHQ_URL)

MONGODB_HOST = o.hostname or 'localhost'
MONGODB_PORT = o.port or 27017
MONGODB_USERNAME = o.username or None
MONGODB_PASSWORD = o.password or None
MONGODB_DATABASE = o.path.strip('/') or None


# other stuff

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SENTRY_DSN = os.environ.get('SENTRY_DSN')
RAVEN_CONFIG = {
    'dsn': SENTRY_DSN,
}

REDISCLOUD_URL = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379')

AUTORELOAD_SUBSCRIBERS = os.environ.get('AUTORELOAD_SUBSCRIBERS', False)
