import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-97x=#7ol0tedgvc5g6d+hsxw*l@y7_60p$(hld=h9ax&e34&td'

# SECURITY WARNING: don't run with debug turned on in production!
ENV_DEBUG: str = os.environ.get("DASH_DEBUG", "on").lower()
if ENV_DEBUG in ("on", "true", "1"):
    DEBUG = True
elif ENV_DEBUG in ("off", "false", "0"):
    DEBUG = False
else:
    raise ValueError("Invalid DONITO_DEBUG value")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "dash-x52b.onrender.com"]
CSRF_TRUSTED_ORIGINS = [
    "https://dash-x52b.onrender.com",
    "http://localhost",
    "http://127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'web',
    'tailwind',
    'theme'
]
if DEBUG:
    INSTALLED_APPS.append('django_browser_reload')

INTERNAL_IPS = [
    "127.0.0.1",
]
TAILWIND_APP_NAME = 'theme'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
      "django_browser_reload.middleware.BrowserReloadMiddleware",
]

ROOT_URLCONF = 'server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'server.wsgi.application'


# Database https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": (
        {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
        if DEBUG
        else {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DASH_DB_NAME"),
            "USER": os.environ.get("DASH_DB_USER"),
            "PASSWORD": os.environ.get("DASH_DB_PASSWORD"),
            "HOST": os.environ.get("DASH_DB_HOST"),
            "PORT": "5432",
        }
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'
#STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# powerbi
PBI_TENANT_ID = "9df9ef0a-de86-4a17-876b-cee87cdd4b94"
PBI_CLIENT_ID = "ceef888d-a35e-47f9-858a-e8d4105f2e80"
PBI_CLIENT_SECRET = "4VJ8Q~4JpzSdJGqAzN1XX6bPGKeTIigqqA3aicKU"
PBI_AUTHORITY = f"https://login.microsoftonline.com/{PBI_TENANT_ID}"
PBI_REDIRECT_URI = "https://dash-x52b.onrender.com/azure-callback"
PBI_GROUP_ID = "0b6d4684-0b88-4282-86b2-1d7001262130"
PBI_REPORT_ID = "ffcae09c-4d62-4807-bf49-aee01e974899"
PBI_SCOPES = ["https://analysis.windows.net/powerbi/api/.default"]

AUTH_USER_MODEL = "core.User"
LOGIN_URL = "/login"

