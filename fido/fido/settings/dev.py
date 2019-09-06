from .base import *  # noqa

INSTALLED_APPS += (
    'forecast_prototype',
    'webpack_loader',
)

STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "front_end", "fido", "build", "static"),
    "/fido/front_end/fido/build/static",
    "/fido/front_end/fido/dist/static",
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "front_end/fido/build/",  # must end with slash
        "STATS_FILE": "/fido/front_end/fido/build/webpack-stats.json"  #os.path.join(BASE_DIR, "front_end", "fido", "build", "webpack-stats.json"),
    }
}

# for debug_toolbar, to activate it only on localhost
INTERNAL_IPS = ['127.0.0.1']
