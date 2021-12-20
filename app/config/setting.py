import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(f"{BASE_DIR}{Path('/.env')}", override=True)

version = os.getenv('API_VERSION')

secret_key = os.getenv('SECRET_KEY')
debug_mode = os.getenv('FLASK_DEBUG', False) == 'True'
env_mode = os.getenv('FLASK_ENV', 'test')
port = os.getenv('FLASK_PORT', '5000')
host = os.getenv('FLASK_HOST', '0.0.0.0')
api_domain = os.getenv('API_DOMAIN')

auth_token_expire_sec = int(os.getenv('AUTH_TOKEN_EXPIRE_SEC'))

# Redis Setting
redis_host = os.getenv('REDIS_HOST')
redis_port = int(os.getenv('REDIS_PORT'))
redis_password = os.getenv('REDIS_PASSWORD')
red_is_ssl = True if os.getenv('REDIS_SSL') == 'True' else False

# MongoDB Setting
mongo_host = os.getenv('MONGO_HOST')
mongo_port = os.getenv('MONGO_PORT')
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_auth_db = os.getenv('MONGO_AUTH_DB_NAME')
mongo_conn_url = os.getenv('MONGO_CONN_URI')
# mongo_timeout_sec = int(os.getenv('MONGO_TIMEOUT'))
# mongo_ssl = True if os.getenv('MONGO_SSL') == 'True' else False
# mongo_allow_invalid_hostnames = True if os.getenv('MONGO_ALLOW_INVALID_HOSTNAMES') == 'True' else False
# mongo_allow_invalid_cert = True if os.getenv('MONGO_ALLOW_INVALID_CERT') == 'True' else False

verify_exception_paths = [
    '/',
    '/favicon.ico',
    '/register',
    '/login',
]
