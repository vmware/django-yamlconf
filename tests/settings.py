"""Django settings for tests."""

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production

DEBUG = False
SECRET_KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

LOGGING = {  # avoids spurious output in tests
    "version": 1,
    "disable_existing_loggers": True,
}


# Application definition

INSTALLED_APPS = [
    "django_yamlconf",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


MEDIA_URL = "/media/"  # Avoids https://code.djangoproject.com/ticket/21451

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory",
    },
}

ROOT_URLCONF = "tests.urls"

TEMPLATES = [
    {
        "NAME": "jinja2",
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "APP_DIRS": True,
        "DIRS": [],
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, "tests", "static")

STATIC_URL = "/static/"

STATICFILES_DIRS = []

# Cache and database

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
