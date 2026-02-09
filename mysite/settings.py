from pathlib import Path
import os

# ---------------------------------
# BASE DIRECTORY
# ---------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------
# SECURITY
# ---------------------------------
SECRET_KEY = 'change-this-secret-key'
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'hakimu.onrender.com']

# ---------------------------------
# APPLICATIONS
# ---------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # your app
    'core',
]

SITE_ID = 1

# ---------------------------------
# MIDDLEWARE
# ---------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'
WSGI_APPLICATION = 'mysite.wsgi.application'

# ---------------------------------
# TEMPLATES
# ---------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'core' / 'templates'],
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

# ---------------------------------
# DATABASE
# ---------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ---------------------------------
# PASSWORD VALIDATION
# ---------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ---------------------------------
# INTERNATIONALIZATION
# ---------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ---------------------------------
# STATIC FILES (Render + WhiteNoise)
# ---------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'core' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ---------------------------------
# DEFAULT PRIMARY KEY
# ---------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------
# AUTHENTICATION BACKENDS
# ---------------------------------
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ---------------------------------
# ALLAUTH SETTINGS (NEW STYLE)
# ---------------------------------
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'