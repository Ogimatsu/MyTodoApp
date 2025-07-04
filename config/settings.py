import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# .env を読み込む
load_dotenv(BASE_DIR / ".env", override=True)

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

if DEBUG:
    # 開発用
    SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'unsafe-dev-key')
    if SECRET_KEY == 'unsafe-dev-key':
        import warnings
        warnings.warn("<i class='bi bi-exclamation-triangle-fill'></i> 開発用SECRET_KEYが使用されています。")
else:
    # 本番用
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

ALLOWED_HOSTS = [
    'my-task-app.click',        # 独自ドメイン
    'www.my-task-app.click',    # www付きの場合
    '18.178.182.68',            # Elastic IP
    'localhost',                # ローカル環境の確認用
    '127.0.0.1',                # ローカルIP（ローカルテスト用）
]

CSRF_TRUSTED_ORIGINS = ['https://my-task-app.click', 'https://www.my-task-app.click']

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Application definition

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'todos.apps.TodoConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'django_recaptcha',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'config.validators.CustomMinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 日時の記載方法
DATETIME_FORMAT = 'Y/m/d H:i'
DATE_FORMAT = 'Y/m/d'
TIME_FORMAT = 'H:i:s'

# ログイン後に遷移するページ
LOGIN_REDIRECT_URL = '/'
# @login_required 時のリダイレクト先
LOGIN_URL = '/login/'
# ログアウト後の遷移先
LOGOUT_REDIRECT_URL = '/login/'

# パスワード再発行用
if DEBUG:
    # 開発用
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # 本番用
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST')
    EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', 587))
    EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_PASSWORD')
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')

# カスタムユーザーモデルの指定
AUTH_USER_MODEL = 'users.CustomUser'

# メッセージストレージの切り替え
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    # ログのフォーマット
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    # ログファイルの出力先
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
            'formatter': 'verbose',
        },
    },
    # Django本体や、自分のアプリで logger を使った場合の設定
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# httpsにする設定
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_HSTS_SECONDS = 31536000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_SITE_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_SECRET_KEY')