"""
Django settings for RepoDir project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Monkey patch due to mptt_admin trying to import something that hass been removed.
from django.utils.translation import ugettext_lazy
from django.contrib.admin.views import main
main.EMPTY_CHANGELIST_VALUE = ugettext_lazy('(None)')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd370j#0dz6xa%^p7ym(9#=q64jej(r*5e#c4p$^$@r8q_geplv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Live site

FROM_EMAIL = 'copdess-noreply@copdessdirectory.osf.io'

# Sendgrid
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = "CHANGEME"

# Application definition

INSTALLED_APPS = (
    'dor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework_swagger',
    'robots',
    'mptt',
    'django_mptt_admin',
    # 'pipeline'
)

SITE_ID = 1

# ROBOTS_USE_SITEMAP = False

# STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
#
# AWS_PRELOAD_METADATA = True
#
# PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
# PIPELINE_CSSMIN_BINARY = 'cssmin'
# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'
#
# PIPELINE_CSS = {
#     'dor_css': {
#         'source_filenames': (
#             'bower_components/bootstrap/dist/css/bootstrap.css',
#             'css/main.css',
#             'css/normalize.css',
#         ),
#         'output_filename': 'min.css',
#         'variant': 'datauri',
#     },
# }
# PIPELINE_JS = {
#     'dor_js': {
#         'source_filenames': (
#             'bower_components/jquery/dist/jquery.js',
#             'bower_components/bootstrap/dist/css/bootstrap.js',
#             'js/plugins.js',
#         ),
#         'output_filename': 'min.js',
#     }
# }

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'RepoDir.urls'

WSGI_APPLICATION = 'RepoDir.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)),'static')),)
