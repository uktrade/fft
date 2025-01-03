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

    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--enable-debugpy",
            action="store_true",
            help="Enable debugpy for remote debugging",
        )

    def run(self, *args, **options):
        if options["enable_debugpy"]:
            initialize_debugpy()

        super().run(*args, **options)
