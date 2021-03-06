import json
import os
from os.path import abspath, dirname

from django.contrib.messages import constants as message_constants
from django.core.exceptions import ImproperlyConfigured


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = abspath(dirname(dirname(dirname(__file__))))
ROOT = lambda *wargs: os.path.join(BASE_DIR, *wargs)

with open(os.path.join(BASE_DIR, 'secret_key.json')) as f:
    json_data = json.loads(f.read())
    secret_keys = json_data['SECRET_KEYS']
    dev_databases = json_data['DEV_DATABASES']
    prod_databases = json_data['PROD_DATABASES']
    fcm_server_key = json_data['FCM_SERVER_KEY']


def get_json_data(key_name, data_dic):
    try:
        return data_dic[key_name]
    except KeyError:
        error_msg = 'Set the {} environment variable'.format(key_name)
        raise ImproperlyConfigured(error_msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gh67^0opf#&o(tg1^h*u%w*-6=k-89236=h+%_gd0q(xfm0!oz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PROJECT_FOLDER = os.getcwd()

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # 'rest_framework',
    # 'rest_framework.authtoken',
    # 'rest_auth',
    # 'allauth',
    # 'allauth.account',
    # 'rest_auth.registration',
    'braces',

    # third apps
    'bootstrap3',
    'disqus',
    # 'crispy_forms',
    'datetimewidget',
    # 'debug_toolbar',
    'django_summernote',
    'social.apps.django_app.default',

    # local apps
    'accounts',
    'recruit',
    'chat',
    ]

# AUTH_USER_MODEL = 'accounts.CustomUser'
AUTH_USER_MODEL = 'accounts.ExtendedUser'

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.twitter.TwitterOAuth',
    # 'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend'
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Google
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

# Twitter
# SOCIAL_AUTH_TWITTER_KEY = ''
# SOCIAL_AUTH_TWITTER_SECRET = ''

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']          # email을 가져오기 위한 설정.
# FACEBOOK_EXTENDED_PERMISSIONS = ['email']


SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'fields': 'id, name, email, age_range, first_name, last_name, picture, gender, locale'
}

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    # 'social.pipeline.partial.save_status_to_session',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    # 'accounts.social.create_user',
    'social.pipeline.user.create_user',
    'accounts.social.save_profile',
    'accounts.social.update_avatar',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',        # locale middleware
]

ROOT_URLCONF = 'basket_together.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ROOT('basket_together', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'basket_together.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, '../database/db.sqlite3'),
#         'USER': 'test',
#         'PASSWORD': '1234qwer'
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'node_modules')
]

# AUTH_PROFILE_MODULE = 'user_profile.UserProfile'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 2

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 2

# change message level: error to danger
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger',
}

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'

# Support customization via settings.
SUMMERNOTE_CONFIG = {
    # Using SummernoteWidget - iframe mode
    'iframe': True,  # or set False to use SummernoteInplaceWidget - no iframe mode

    # Using Summernote Air-mode
    'airMode': False,

    # Use native HTML tags (`<b>`, `<i>`, ...) instead of style attributes
    # (Firefox, Chrome only)
    'styleWithTags': True,

    # Set text direction : 'left to right' is default.
    'direction': 'ltr',

    # Change editor size
    'width': '100%',
    'height': '480',

    # Use proper language setting automatically (default)
    'lang': None,

    # Or, set editor language/locale forcely
    'lang': 'ko-KR',

    # Customize toolbar buttons
    'toolbar': [
        ['style', ['style']],
        ['style', ['bold', 'italic', 'underline', 'clear']],
        ['para', ['ul', 'ol', 'height']],
        ['insert', ['link']],
    ],

    # Need authentication while uploading attachments.
    'attachment_require_authentication': True,

    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func(),

    # You can add custom css/js for SummernoteWidget.
    'css': (
    ),
    'js': (
    ),

    # And also for SummernoteInplaceWidget.
    # !!! Be sure to put {{ form.media }} in template before initiate summernote.
    'css_for_inplace': (
    ),
    'js_for_inplace': (
    ),

    # You can disable file upload feature.
    'disable_upload': False,

    # Codemirror as codeview
    'codemirror': {
            # Please visit http://summernote.org/examples/#codemirror-as-codeview
            'theme': 'monokai',
    },

}

# secret keys
DISQUS_WEBSITE_SHORTNAME = get_json_data('DISQUS_WEBSITE_SHORTNAME', secret_keys)
GOOGLE_MAP_API_KEY = get_json_data('GOOGLE_MAP_API_KEY', secret_keys)
GOOGLE_ANALYTICS_TRACKING_ID = get_json_data('GOOGLE_ANALYTICS_TRACKING_ID', secret_keys)

FCM_SERVER_KEY = fcm_server_key
