from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (
'django-insecure-@56xgy7m+&wa&7+w)2%7gklgp2bm1nj2puz&jfav72@icqjo^^'
)

DEBUG = True

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
AUTH_USER_MODEL = 'users.CustomUser'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig',
    'djoser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
                'password_validation.'
                'NumericPasswordValidator',
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

DJOSER = {
       'LOGIN_FIELD': 'email',
       'SERIALIZERS': {
           'user_create': 'users.serializers.UserRegistrationSerializer',
           'user': 'users.serializers.CustomUserSerializer',
           'current_user': 'users.serializers.CustomUserSerializer',
       },
       'USER_ID_FIELD': 'id',
       'HIDE_USERS': False,
       'PERMISSIONS': {
           'user': ['rest_framework.permissions.IsAuthenticated'],
           'user_list': ['rest_framework.permissions.AllowAny']
       },
   }

SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(days=60),
   'AUTH_HEADER_TYPES': ('Bearer',),
}

STATIC_URL = '/static/'

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
