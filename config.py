import os

UA_KEY = os.environ.get('UA_KEY')
UA_SECRET = os.environ.get('UA_SECRET')
UA_MASTER = os.environ.get('UA_MASTER')
AUTORELOAD_SUBSCRIBERS = os.environ.get('AUTORELOAD_SUBSCRIBERS', False)

MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_PORT = os.environ.get('MONGODB_PORT', 27017)
MONGODB_DATABASE = os.environ.get('MONGODB_DATABASE', 'norrin')
MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME')
MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
