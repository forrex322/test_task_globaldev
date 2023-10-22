import sys
import environ

# globaldev_app/config/settings.py - 2 = globaldev_app/
ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("globaldev_app")
sys.path.append("globaldev_app/apps")

# Environment
# https://django-environ.readthedocs.io/en/latest/#how-to-use
# ------------------------------------------------------------------------------
env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_SECRET_KEY=(str, ""),
    DJANGO_ADMINS=(list, []),
    DJANGO_ALLOWED_HOSTS=(list, []),
    # Static/Media
    DJANGO_STATIC_ROOT=(str, str(APPS_DIR("staticfiles"))),
    DJANGO_MEDIA_ROOT=(str, str(APPS_DIR("media"))),
    # Debug
    DJANGO_USE_DEBUG_TOOLBAR=(bool, False),
    DJANGO_TEST_RUN=(bool, False),
    DJANGO_DEBUG_SQL=(bool, False),
    DJANGO_DEBUG_SQL_COLOR=(bool, False),
    # CORS
    DJANGO_CORS_ORIGIN_WHITELIST=(list, []),
    DJANGO_CORS_ALLOW_HEADERS=(tuple, ()),
    DJANGO_CORS_ORIGIN_ALLOW_ALL=(bool, False),
    # Database
    POSTGRES_HOST=(str, "db"),
    POSTGRES_PORT=(int, 5432),
    POSTGRES_DB=(str, ""),
    POSTGRES_USER=(str, ""),
    POSTGRES_PASSWORD=(str, ""),
    # Celery
    DJANGO_CELERY_BROKER_URL=(str, "redis://redis:6379/0"),
    DJANGO_CELERY_BACKEND=(str, "redis://redis:6379/0"),
    DJANGO_CELERY_TASK_ALWAYS_EAGER=(bool, False),
)

# Django Core
# https://docs.djangoproject.com/en/2.2/ref/settings/#core-settings
DEBUG = env.bool("DJANGO_DEBUG")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
SECRET_KEY = env("DJANGO_SECRET_KEY")
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
ADMIN_SITE_TITLE = "globaldev_app"
ADMIN_SITE_HEADER = "globaldev_app"
ADMINS = tuple([tuple(admins.split(":")) for admins in env.list("DJANGO_ADMINS")])
MANAGERS = ADMINS
ADMIN_URL = "admin/"

# Django Sites
# https://docs.djangoproject.com/en/2.2/ref/settings/#sites
# ------------------------------------------------------------------------------
SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("POSTGRES_HOST"),
        "PORT": env("POSTGRES_PORT"),
    }
}

# Django Applications
# https://docs.djangoproject.com/en/2.2/ref/settings/#installed-apps
# ------------------------------------------------------------------------------
DJANGO_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
)
THIRD_PARTY_APPS = (
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "corsheaders",
    "rest_auth",
    "rest_auth.registration",
    "oauth2_provider",
)
LOCAL_APPS = (
    "users.apps.UsersConfig",
    "taskapp.apps.TaskAppConfig",
    "booktimetracker.apps.BooktimetrackerConfig",
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Django Templates
# https://docs.djangoproject.com/en/2.2/ref/settings/#templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(APPS_DIR.path("templates")),
        ],
        "OPTIONS": {
            "debug": DEBUG,
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Django Static Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#static-files
# ------------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = env("DJANGO_STATIC_ROOT")
STATICFILES_DIRS = (str(APPS_DIR.path("static")),)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Django Media Files
# https://docs.djangoproject.com/en/2.2/ref/settings/#media-root
# ------------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = env("DJANGO_MEDIA_ROOT")

# Celery
# http://docs.celeryproject.org/en/latest/userguide/configuration.html
# ------------------------------------------------------------------------------
CELERY_BROKER_URL = env("DJANGO_CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("DJANGO_CELERY_BACKEND")
if env.bool("DJANGO_TEST_RUN") or any("pytest" in arg for arg in sys.argv):
    CELERY_TASK_ALWAYS_EAGER = True
else:
    CELERY_TASK_ALWAYS_EAGER = env.bool("DJANGO_CELERY_TASK_ALWAYS_EAGER")

# Django Auth
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
AUTH_USER_MODEL = "users.User"
LOGIN_URL = "api:users:auth:login"
LOGIN_REDIRECT_URL = "/"

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_USER_EMAIL_FIELD = "email"
# Django REST Framework
# https://www.django-rest-framework.org/api-guide/settings/
# ------------------------------------------------------------------------------
PAGE_SIZE = 10
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.BasicAuthentication",
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": PAGE_SIZE,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# API Documentation: drf-yasg
# https://drf-yasg.readthedocs.io/en/stable/settings.html
# ------------------------------------------------------------------------------
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "PERSIST_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "Token": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        }
    },
}

# django-rest-auth
# https://django-rest-auth.readthedocs.io/en/latest/configuration.html
# ------------------------------------------------------------------------------
LOGOUT_ON_PASSWORD_CHANGE = False
OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    "TOKEN_SERIALIZER": "users.serializers.TokenSerializer",
}
REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "users.serializers.RegisterSerializer",
}
