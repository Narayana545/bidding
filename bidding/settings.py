"""
Django settings for bidding project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vhzy_m5%i=mo*cq4+j$i5-2)kc_9s+%&t5s+dkz5ck_%m5dhhs'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts',
    'items',
    # 'paypal.standard.ipn',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'bidding.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

WSGI_APPLICATION = 'bidding.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bid',
        'HOST':'localhost',
        'PASSWORD':'root',
        'USER':'root',
        'PORT':'3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL='/media/'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
EMAIL_USE_TLS = True  
EMAIL_USE_SSL =False
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587
EMAIL_HOST_USER = 'onlineauction305@gmail.com'  
EMAIL_HOST_PASSWORD = "cmpb yjrj gpky kmoz"
# This is important for password reset links
DEFAULT_FROM_EMAIL = 'sivanarayana545@gmail.com'


PAYPAL_CLIENT_ID = 'AUElc0qVnoraW7rTeBDDB3MnJVVcMdKA-FWXqqMqv_HJZCv8Qw__0txBvbqPMfrylZz-_SMukOQVQ2AE'
PAYPAL_CLIENT_SECRET = 'EL3_9YoYKTTq49VJCnHhXdLrSNcWCzIOKSmiuCQt3sqyF14-AUDxEQvlfvMf3diVwRG0i2rKbZH1CVgp'
PAYPAL_MODE = 'sandbox'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
 ]

STATIC_ROOT = os.path.join(BASE_DIR,'assets')