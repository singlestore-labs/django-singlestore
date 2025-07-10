import os

DJANGO_SETTINGS_MODULE = 'singlestore_settings'

DATABASES = {
    "default": {
        "ENGINE": "django_singlestore",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": os.environ.get("SINGLESTORE_PASSWORD", ""),
        "NAME": "django_db",
    },
    "other": {
        "ENGINE": "django_singlestore",
        "HOST": "127.0.0.1",
        "PORT": 3306,
        "USER": "root",
        "PASSWORD": os.environ.get("SINGLESTORE_PASSWORD", ""),
        "NAME": "django_db_other",
    },
}


USE_TZ = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SECRET_KEY = 'your-unique-secret-key-here'
