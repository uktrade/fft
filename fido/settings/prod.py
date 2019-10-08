from .base import *  # noqa

SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join(env('NODE_PATH'), '/govuk-frontend/govuk/all'),
]
