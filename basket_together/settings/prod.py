from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

# Django 내 암호화 시에 salt 값으로 사용.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

DATABASES = {
    'default': {
        'ENGINE': get_json_data('ENGINE', prod_databases['default']),
        'NAME': get_json_data('NAME', prod_databases['default']),
        'USER': get_json_data('USER', prod_databases['default']),
        'PASSWORD': get_json_data('PASSWORD', prod_databases['default']),
        'HOST': get_json_data('HOST', prod_databases['default']),
    },
}

SOCIAL_AUTH_FACEBOOK_KEY = get_json_data('PROD_SOCIAL_AUTH_FACEBOOK_KEY', secret_keys)
SOCIAL_AUTH_FACEBOOK_SECRET = get_json_data('PROD_SOCIAL_AUTH_FACEBOOK_SECRET', secret_keys)