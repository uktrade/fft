import os
import sys

from django.core.management.commands.runserver import Command as RunserverCommand


def initialize_debugpy():
    import debugpy

    try:
        debugpy.listen(("0.0.0.0", 5678))
        sys.stdout.write("debugpy listening on port 5678...\n")
    except Exception as exc:
        sys.stderr.write(f"Failed to initialize debugpy: {exc}\n")


class Command(RunserverCommand):

    def run(self, *args, **options):
        ENABLE_DEBUGPY = os.getenv("ENABLE_DEBUGPY")
        if ENABLE_DEBUGPY and ENABLE_DEBUGPY.lower() == "true":
            initialize_debugpy()

        super().run(*args, **options)
