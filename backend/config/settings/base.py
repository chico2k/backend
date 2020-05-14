import os
import environ

# Base Dir in Docker /home/app
BASE_DIR = (
    environ.Path(__file__) - 3
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=1))

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'oauth2_provider',
    'corsheaders',
    'rest_framework',
    # 'rest_framework.authtoken',
    'djoser',

    # # Custom Apps
    'main',
    'users',
    'profiles',
    'sports',
    'reviews',
    'experiences',
    'location',
    'certificates',
    'search_indexes',

]


# Custom User Model
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope', 'groups': 'Access to your groups'}
}


ROOT_URLCONF = 'main.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'main/notifications'), ],
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

WSGI_APPLICATION = 'main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", 'django.db.backends.sqlite3'),
        "NAME": os.environ.get("DB_DATABASE", 'db'),
        "USER": os.environ.get("DB_USER", 'db_user'),
        "PASSWORD": os.environ.get("DB_PASSWORD", 'db_pw'),
        "HOST": os.environ.get("DB_HOST", ""),
        "PORT": os.environ.get("DB_PORT", ""),
    }
}

print("DB_---------------------------")
print(DATABASES)

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# RESTFRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',

    ),
    'DEFAULT_PAGINATION_CLASS': 'main.management.pagination.pagination.PageNumberPaginationWithCount',
    'PAGE_SIZE': 10,
}


DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'http://localhost:3000/auth/password/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'http://localhost:3000/auth/password/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'http://localhost:3000/auth/activate/send/{uid}/{token}',
    'EMAIL': {
        'activation': 'main.email.ActivationEmail',
        'confirmation': 'main.email.ConfirmationEmail',
        'password_reset': 'main.email.PasswordResetEmail',
        'password_changed_confirmation': 'main.email.PasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'main.email.UsernameChangedConfirmationEmail',
        'username_reset': 'main.email.UsernameResetEmail',
    },
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': 'True',
    'SET_USERNAME_RETYPE': 'True',
    'SET_PASSWORD_RETYPE': 'True',
    'SEND_ACTIVATION_EMAIL': 'True',
    'TOKEN_MODEL': None,
    'SEND_CONFIRMATION_EMAIL': 'True',
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': 'True',
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': 'True',
    "PERMISSIONS":
    {
        "activation": ["rest_framework.permissions.AllowAny"],
        "password_reset": ["rest_framework.permissions.AllowAny"],
        "password_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_password": ["djoser.permissions.CurrentUserOrAdmin"],
        "username_reset": ["rest_framework.permissions.AllowAny"],
        "username_reset_confirm": ["rest_framework.permissions.AllowAny"],
        "set_username": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_create": ["rest_framework.permissions.AllowAny"],
        "user_delete": ["djoser.permissions.CurrentUserOrAdmin"],
        "user": ["djoser.permissions.CurrentUserOrAdmin"],
        "user_list": ["djoser.permissions.CurrentUserOrAdmin"],
        "token_create": ["rest_framework.permissions.AllowAny"],
        "token_destroy": ["rest_framework.permissions.IsAuthenticated"],
    },
}
