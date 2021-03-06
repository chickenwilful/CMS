"""
Django settings for storm project.


For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import storm

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

#DJANGO_SETTINGS_MODULE

DJANGO_SETTINGS_MODULE = 'storm.settings'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k(^rpfggogw8&79)g3vjno8=7e*dms%ia8ers97w7u1@=ys#vu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'event',
    'post',
    'user',
    'main',
    'storm_user',
    'socialnetwork',
    'bootstrap3',
    'crossdomainxhr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'crossdomainxhr.XsSharing',
)

ROOT_URLCONF = 'storm.urls'

WSGI_APPLICATION = 'storm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storm',
        'USER': 'storm_user',
        'PASSWORD': 'storm_pass',
        'HOST': '127.0.0.1', # Using direct IP instead of localhost, to ensure MySQLdb doesn't fail
    },
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'sqlite_test'
        }
    }

# #For testing
# if 'test' in sys.argv:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': 'test',
#             'USER': 'storm_user',
#             'PASSWORD': 'storm_pass',
#             'HOST': '127.0.0.1',
#         },
#     }


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Singapore'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Logging settings

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'storm': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # default
)
ANONYMOUS_USER_ID = -1

#for extending user

AUTH_PROFILE_MODULE = 'storm_user.UserProfile'

# Twitter API keys

TWITTER_KEY = 'arB30953S5DXoJgr3nCw'
TWITTER_SECRET = 'zKdhSygOjx6xYTaT7XeZzT9EzWM0fK0gDY7IH6slI'

# Facebook API keys

FACEBOOK_APP_ID = '296241580500537'
FACEBOOK_SECRET = '3885761cc214d22bbae1aee273b789be'

# Google+ API keys

GPLUS_APP_ID = '531d584d9536407631000074'
GPLUS_SECRET = '2ec5211f312e30f87fdc47b730e65aad'

# Tumblr API keys

TUMBLR_APP_ID = 'yScYcn5Ev5c78caQ447cTQFnPQRo0LTRrdfHW5i2G98cAvfVyX'
TUMBLR_SECRET = 'JKpFXPn4Y6ofpwwRfBREboqVuIEgPw2BX5iDSEtCTx5SQxZGtX'


BOOTSTRAP3 = {
    'jquery_url': '//code.jquery.com/jquery.min.js',
    'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.0.3/',
    'css_url': None,
    'theme_url': None,
    'javascript_url': None,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-8',
}