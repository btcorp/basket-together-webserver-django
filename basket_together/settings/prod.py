from .common import *

DEBUG = False

ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

# Django 내 암호화 시에 salt 값으로 사용.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', SECRET_KEY)

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'ubuntu',
#         'USER': 'ubuntu',
#         'PASSWORD': '1234qwer',
#         'HOST': '127.0.0.1',
#     }
# }

SOCIAL_AUTH_FACEBOOK_KEY = get_env_variable('PROD_SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = get_env_variable('PROD_SOCIAL_AUTH_FACEBOOK_SECRET')
