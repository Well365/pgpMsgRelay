import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["0.0.0.0",
                 "www.si4key.com",
                 "si4key.com",
                 "https://si4key.com",
                 "https://www.si4key.com",
                 "si4key.com:80",
                 "www.si4key.com:80",
                 "si4key.com:443",
                 "www.si4key.com:443",
                 "8.219.85.168",
                 "172.19.41.215",
                 "localhost"
                 ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'message_agent',
    'rest_framework',  # 添加REST Framework
    'corsheaders',  # 添加CORS支持
    'django.contrib.sites',  # 添加django.contrib.sites
    'django.contrib.sitemaps',  # 添加django.contrib.sitemaps
    'django.contrib.flatpages',  # 添加django.contrib.flatpages
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 添加在最前面
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 确保这行在正确位置
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pgp_message.urls'

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
                'message_agent.context_processors.languages',  # 添加自定义上下文处理器
            ],
        },
    },
]

WSGI_APPLICATION = 'pgp_message.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

# 国际化设置
LANGUAGE_CODE = 'en'  # 默认语言
LANGUAGE_SESSION_KEY = '_language'
LANGUAGE_COOKIE_NAME = 'django_language'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True
USE_TZ = True

# 支持的语言
LANGUAGES = [
    ('zh-hans', _('简体中文')),
    ('ja', _('日本語')),
    ('en', _('English')),
    ('es', _('Español')),
    ('ar', _('العربية')),
]

# 翻译文件目录
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

# 默认语言cookie设置
LANGUAGE_COOKIE_AGE = None  # 会话结束时过期
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_DOMAIN = None
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = False
LANGUAGE_COOKIE_SAMESITE = None

STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# 新增：指定静态文件收集目录，供 collectstatic 使用
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 添加缓存配置，确保国际化页面不会被缓存
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 60,  # 1分钟
    }
}

# 禁用静态文件缓存
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework 配置
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
}

# CORS 配置，允许所有来源跨域（如需限制可自行调整）
CORS_ALLOW_ALL_ORIGINS = True