
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-iun@so+p=hbx3%)7!+qbd8kzacliac-uu+$(3c6lhpb_434cr('
DEBUG = True
ALLOWED_HOSTS = ['*']

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# 🧠 4️⃣ Installed Apps
INSTALLED_APPS = [
    'jazzmin',
    'mptt',
    'ckeditor',
    'ckeditor_uploader',
    'multiselectfield',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.humanize',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',

    'response.apps.ResponseConfig',
    'projects.apps.ProjectsConfig',
    'properties.apps.PropertiesConfig',
    'utility.apps.UtilityConfig',
    'crm.apps.CrmConfig',
    'user.apps.UserConfig',
    'blog.apps.BlogConfig',

    'easy_thumbnails',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

#  URL & WSGI
ROOT_URLCONF = 'saybanoorjogeshwari.urls'
WSGI_APPLICATION = 'saybanoorjogeshwari.wsgi.application'

#  Templates
TEMPLATES = [
    {   
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utility.context_processors.global_settings_processor',
            ],
        },
    },
]


#  Auth
AUTH_USER_MODEL = 'user.CustomUser'

RECAPTCHA_SITE_KEY = "6Lfs5zssAAAAADMVaU7ADWR-KVRYTiceY2iapH0U"
RECAPTCHA_SECRET_KEY = "6Lfs5zssAAAAAJfTP8yyIQnBzPX6o7QBUIK-_P5Z"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = 'yourgmail@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = 'admin@gmail.com'

# 🔐 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-in'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



# 📌 CKEditor
CKEDITOR_UPLOAD_PATH = "uploads/"

# 📌 Site Framework
SITE_ID = 1

# 📌 Auth Redirects
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/accounts/login/'

# 📌 Message tags for bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# ✅ End of File
