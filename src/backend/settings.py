"""
Following env vars need to be configured in prod env:
IS_PROD: notify that this is a prod deployment
SECRET_KEY: used by django refer to https://docs.djangoproject.com/en/3.0/ref/settings/#secret-key
DATABASE_ENGINE: refer to https://docs.djangoproject.com/en/3.0/ref/settings/#engine
DATABASE_NAME
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
CSRF_COOKIE_DOMAIN
"""

import os
import sys
import logging

LOGGER = logging.getLogger("backend")

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SETTINGS_DIR)

DEBUG = bool(os.environ.get("IS_PROD", True))

ALLOWED_HOSTS = ["*"]
SECRET_KEY = os.environ.get("SECRET_KEY", "_")
if not SECRET_KEY and not DEBUG:
    raise Exception("You're trying to run production without setting the SECRET_KEY env var")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "rest_api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework.authentication.SessionAuthentication",)
}
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

ROOT_URLCONF = "backend.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "backend.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": os.path.join(BASE_DIR, "db.sqlite3")}}
if not DEBUG and not os.environ.get("DATABASE_HOST"):
    raise Exception("Prod deployment without setting env vars for DATABASE CONNECTION details")
if os.environ.get("DATABASE_HOST"):
    DATABASES = {
        "default": {
            "ENGINE": os.environ["DATABASE_ENGINE"],
            "NAME": os.environ["DATABASE_NAME"],
            "USER": os.environ["DATABASE_USER"],
            "PASSWORD": os.environ["DATABASE_PASSWORD"],
            "HOST": os.environ["DATABASE_HOST"],
            "PORT": os.environ["DATABASE_PORT"],
        }
    }
LOG_LEVEL = "INFO" if DEBUG else "WARNING"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] - [{levelname}] - [{name}.{funcName}:{lineno}] : {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        }
    },
    "handlers": {"console": {"level": LOG_LEVEL, "class": "logging.StreamHandler", "formatter": "verbose"}},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL},
        "backend": {"handlers": ["console"], "level": LOG_LEVEL},
    },
}
# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LOGOUT_REDIRECT_URL = "/"
# CSRF config
CSRF_COOKIE_DOMAIN = os.environ.get("CSRF_COOKIE_DOMAIN", "localhost")
CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_COOKIE_DOMAIN", None) or ["localhost", "127.0.0.1"]

CSRF_COOKIE_SECURE = not DEBUG  # Force the cookie to transit via HTTPS in prod
CSRF_USE_SESSIONS = False  # False then Angular can use it
CSRF_COOKIE_HTTPONLY = False
# SSL config
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# CORS config
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    "x-requested-with",
    "x-csrftoken",
    "content-type",
    "accept",
    "origin",
    "authorization",
    "as-standard-user",
)

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "/static"

TESTING = "test" in "".join(sys.argv)
if TESTING:
    DEBUG = False
    TEMPLATE_DEBUG = False
    PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
    MIDDLEWARE_CLASSES = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
    ]
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}}
