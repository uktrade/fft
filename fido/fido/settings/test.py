from .base import *  # noqa
from .dev import *  # noqa

DATABASES = {
    'default': env.db('aaa', default='psql://postgres:postgres@db:5432/fido_test')
}

