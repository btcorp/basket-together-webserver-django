from .common import *

# Database
DATABASES = {
    'default': {
        'ENGINE': get_json_data('ENGINE', dev_databases['default']),
        'NAME': get_json_data('NAME', dev_databases['default']),
        'USER': get_json_data('USER', dev_databases['default']),
        'PASSWORD': get_json_data('PASSWORD', dev_databases['default']),
        'HOST': get_json_data('HOST', dev_databases['default']),
    },
}

SOCIAL_AUTH_FACEBOOK_KEY = get_json_data('DEV_SOCIAL_AUTH_FACEBOOK_KEY', secret_keys)
SOCIAL_AUTH_FACEBOOK_SECRET = get_json_data('DEV_SOCIAL_AUTH_FACEBOOK_SECRET', secret_keys)
