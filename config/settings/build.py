"""
Minimum base settings required to build an OCI image when compiling statics during build phase.
manage.py compilestatic --settings=config.settings.build
"""
import os


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

SECRET_KEY = "dont-use-in-prod"

ALLOWED_HOSTS = "*"

INSTALLED_APPS = [
    "user",
    "authbroker_client",
    "future_years.apps.FutureYearsConfig",
    "upload_split_file.apps.UploadSplitFileConfig",
    "oscar_return.apps.OscarReturnConfig",
    "previous_years.apps.PreviousYearsConfig",
    "forecast.apps.ForecastConfig",
    "gifthospitality.apps.GifthospitalityConfig",
    "costcentre.apps.CostCentreConfig",
    "chartofaccountDIT.apps.ChartAccountConfig",
    "treasuryCOA.apps.TreasuryCOAConfig",
    "treasurySS.apps.TreasurySSConfig",
    "core.apps.CoreConfig",
    "end_of_month.apps.EndOfMonthConfig",
    "importdata.apps.ImportDataConfig",
    "upload_file.apps.UploadFileConfig",
    "download_file.apps.DownloadFileConfig",
    "pingdom.apps.PingdomConfig",
    "data_lake.apps.DataLakeConfig",
    "mi_report_data.apps.MiReportDataConfig",
    "django_extensions",
    "django_tables2",
    "django_filters",
    "django_admin_listfilter_dropdown",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap_breadcrumbs",
    "dal",
    "dal_select2",
    "storages",
    "sass_processor",
    "guardian",
    "reversion",
    "rest_framework",
    "simple_history",
    "axes",
    "adv_cache_tag",
    "django_chunk_upload_handlers",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/' + 'db.sqlite3',
        }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "user.User"
AUTHBROKER_URL = "dont-use-in-prod"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "front_end/build/static"),
    os.path.join(BASE_DIR, "node_modules/govuk-frontend"),
)

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
