"""
Django settings for bashoneliners project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(p^8-@2q(uck=2+fph+1pxx=)4lrl)_!p%7b9m1&#qoy%+9+v6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'oneliners',
    # Required by sitemaps.
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django_distill',
    'flags',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bashoneliners.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'oneliners.context_processors.google_analytics',
            ],
        },
    },
]

WSGI_APPLICATION = 'bashoneliners.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Required when using the "staticfiles" app.
STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Usage example:
# import logging
# logger = logging.getLogger(__name__)
# logger.debug('something happened')
LOGS_DIR = BASE_DIR / 'logs'

LOGGING = {
    "version": 1,
    # Merge with default: https://docs.djangoproject.com/en/4.2/ref/logging/#default-logging-configuration
    # Merge logic explained: https://docs.djangoproject.com/en/4.2/topics/logging/#configuring-logging
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {name} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "info-file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "info.log",
            "level": "INFO",
            "formatter": "verbose",
        },
        "error-file": {
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "error.log",
            "level": "ERROR",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {
            "handlers": ["info-file", "error-file"],
            "level": "DEBUG",
        },
    },
}

#
# Project specific Django settings.
#

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google.GoogleOAuth',
    'social_core.backends.twitter.TwitterOAuth',
)

# Enable Visit on site link on Django Admin from User entries.
ABSOLUTE_URL_OVERRIDES = {
    "auth.user": lambda o: f"/oneliners/users/{o.pk}/",
}

# Make Django write to file when it would email Admin.
EMAIL_FILE_PATH = LOGS_DIR / 'emails'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

LOGIN_URL = '/oneliners/login/'
LOGIN_REDIRECT_URL = '/oneliners/login/'

FLAGS = {
    # 'DEPLOYMENT_LINKS': [{'condition': 'boolean', 'value': True}],
    # 'LOGIN': [{'condition': 'boolean', 'value': True}],
    # 'ONELINERS_TABS': [{'condition': 'boolean', 'value': True}],
    # 'PROFILE_TABS': [{'condition': 'boolean', 'value': True}],
    # 'SEARCH': [{'condition': 'boolean', 'value': True}],
    # 'CATEGORIES_FILTER': [{'condition': 'boolean', 'value': True}],
    # 'COMMANDS_FILTER': [{'condition': 'boolean', 'value': True}],
    # 'PAGINATION': [{'condition': 'boolean', 'value': True}],
    # 'VOTING': [{'condition': 'boolean', 'value': True}],
    # 'DJANGO_SITE': [{'condition': 'boolean', 'value': True}],
}

#
# Project specific non-Django settings.
#

# Credentials for posting Tweets on behalf of @bashoneliners.
# Only admin uses it.
TWITTER = {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token': '',
    'access_token_secret': '',
}

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/oneliners/'
SOCIAL_AUTH_LOGIN_URL = '/'

# Login with Google.
# Requires registering a "OAuth 2.0 Client ID" of type "Web application".
# Managed on Google Developer Console: https://console.developers.google.com/
#
# First-time setup:
#   Create an app
#   Create credential
#   Authorized JavaScript origins example: https://bashoneliners.com
#   Authorized redirect URIs example: https://bashoneliners.com/oauth/complete/google-oauth2/
#   -> All deployments can share this app, just add all URIs to authorize:
#       https://www.bashoneliners.com/oauth/complete/google-oauth2/
#       https://beta.bashoneliners.com/oauth/complete/google-oauth2/
#       http://localhost:8000/oauth/complete/google-oauth2/
#
# See also:
#   http://python-social-auth.readthedocs.org/en/latest/backends/google.html#google-openid
#
# The "Client ID" field of the OAuth 2.0 Client ID.
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
# The "Client secret" field of the OAuth 2.0 Client ID.
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
# In Library, search for "google+" and enable "Google+ API"
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
]

# Login with GitHub.
# Requires creating an "OAuth App".
# Managed under: Settings / Developer setings / OAuth Apps
#
# First-time setup:
#   Create an app: https://github.com/settings/applications/new
#       or on https://github.com/settings/developers "New OAuth App" button
#       under Settings / Developer setings / OAuth Apps
#   The most important field is "Authorization callback URL",
#   and since only one URL is allowed per app, separate apps are
#   needed for separate deployments:
#       https://www.bashoneliners.com/oauth/complete/github/
#       https://beta.bashoneliners.com/oauth/complete/github/
#       http://localhost:8000/oauth/complete/github/
#
# See also:
#   https://github.com/settings/developers
#   http://python-social-auth.readthedocs.org/en/latest/backends/github.html
#
# The "Client ID" field of the app.
SOCIAL_AUTH_GITHUB_KEY = ''
# **Generate a new client secret** (never visible again)
SOCIAL_AUTH_GITHUB_SECRET = ''
# App for prod: https://github.com/settings/applications/273862
# App for beta: https://github.com/settings/applications/2316907
# App for local dev: https://github.com/settings/applications/2316903

# Login with Twitter.
# Using the default project in the developer portal, the only free option.
#
# First-time setup:
#   Open the default app under https://developer.twitter.com/en/portal/projects
#   Follow setup steps under "User authentication settings"
#   Type of App: "Web App, Automated App or Bot"
#   Callback URI / Redirect URL:
#       https://www.bashoneliners.com/oauth/complete/twitter/
#       https://beta.bashoneliners.com/oauth/complete/twitter/
#       http://localhost:8000/oauth/complete/twitter/
#
# See also:
#   http://python-social-auth.readthedocs.org/en/latest/backends/twitter.html
#   https://realpython.com/blog/python/adding-social-authentication-to-django/
#
# Under Keys and tokens / Consumer Keys / API Key and Secret
SOCIAL_AUTH_TWITTER_KEY = ''
# **Regenerate** (never visible again)
SOCIAL_AUTH_TWITTER_SECRET = ''

# https://platform.openai.com/account/api-keys
OPENAI_API_KEY = ''
