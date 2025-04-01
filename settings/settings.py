# -*-coding:UTF-8-*-
"""
Django settings for library project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path
from urllib import parse

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*=2!e^c5u^a8!-!-6u=suux)jx!@77s-jcw5h-q^t!+9&e6t)0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'corsheaders',  # 跨域请求
    'apps.basic',
    'apps.library',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.library.middleware.RequestLoggingMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'statics', 'templates')],
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

WSGI_APPLICATION = 'wsgi.application'
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
}

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root'
    }
}

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = 'modops#2020'

CELERY_BROKER_URL = 'redis://:{}@{}:{}/13'.format(parse.quote(REDIS_PASSWORD), REDIS_HOST,
                                                  REDIS_PORT)  # Broker配置，使用Redis作为消息中间件
CELERY_RESULT_BACKEND = CELERY_BROKER_URL  # BACKEND配置，这里使用redis

CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

CELERY_BEAT_SCHEDULE = {
    'my_task': {
        'task': 'apps.libary.tasks.return_reminder',
        'schedule': crontab(minute=0, hour=8),  # 每天8:00执行
    },
}
# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'data', 'statics')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'statics')]

# CORS
# CORS_ORIGIN_WHITELIST =()
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# 设置请求的头部
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'token',
    'authentication',
    'origin'
)

# CACHE
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/11".format(REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://{}:{}/12".format(REDIS_HOST, REDIS_PORT),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": REDIS_PASSWORD,
        }
    },
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

# LOGGING
LOG_IDR = os.path.join(BASE_DIR, 'logs')
if not os.path.isdir(LOG_IDR):
    os.makedirs(LOG_IDR)
LOG_FPATH = os.path.join(LOG_IDR, 'library.log')
CELERY_FPATH = os.path.join(LOG_IDR, 'library_celery.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s][%(pathname)s][%(filename)s][%(funcName)s][LINE:%(lineno)d][%(levelname)s]:%(message)s',
        },
        'simple': {
            'format': '[%{levelname}s]:%(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'encoding': 'utf8',
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_FPATH,
            'when': 'D',
            'interval': 1,
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'db': {
            'level': 'INFO',
            'class': 'commons.custom_handlers.DbHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'library': {
            'handlers': ['console', 'file', 'db'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console', 'file', 'db'],
            'propagate': False,
        }
    }
}


# SimpleUI
SIMPLEUI_STATIC_OFFLINE = True  # 离线模式运行SimpleUI，（如果不配置，simpleui会连接外网下载样式文件）
