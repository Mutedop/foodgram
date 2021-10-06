import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default=('django-insecure-@56xgy7m+&wa&7+w)'
             '2%7gklgp2bm1nj2puz&jfav72@icqjo^^')
)

DEBUG = False
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'users.User'
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'recipes.apps.RecipesConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
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
        'ENGINE': os.environ.get(
            'DB_ENGINE',
            default='django.db.backends.postgresql'
        ),
        'NAME': os.environ.get('DB_NAME', default='foodgram'),
        'USER': os.environ.get('POSTGRES_USER', default='foodgram'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', default='foodgram'),
        'HOST': os.environ.get('DB_HOST', default='localhost'),
        'PORT': os.environ.get('DB_PORT', default=5432),
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
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 6
}

DJOSER = {
       'LOGIN_FIELD': 'email',
       'SERIALIZERS': {
           'user_create': 'users.serializers.CustomUserCreateSerializer',
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

LANGUAGE_CODE = 'ru-en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
