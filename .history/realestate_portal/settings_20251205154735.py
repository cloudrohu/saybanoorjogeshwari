
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-iun@so+p=hbx3%)7!+qbd8kzacliac-uu+$(3c6lhpb_434cr('
DEBUG = True
ALLOWED_HOSTS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




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

    # 📌 My Apps
    'home',
    'projects.apps.ProjectsConfig',
    'properties',
    'utility',
    'crm',
    'user',
    'blog',

    'thumbnails',
]

# 🧠 5️⃣ Middleware
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

# 🧠 6️⃣ URL & WSGI
ROOT_URLCONF = 'realestate_portal.urls'
WSGI_APPLICATION = 'realestate_portal.wsgi.application'

# 🧠 7️⃣ Templates
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# 🧠 9️⃣ Auth
AUTH_USER_MODEL = 'user.CustomUser'

# 🔐 Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
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
