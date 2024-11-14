import re

from django.forms import ValidationError


def validate_only_letters_numbers_spaces(value, field):
    if not re.match(r"^[a-zA-Z0-9\s]*$", value):
        raise ValidationError(
            f"{ field } can only contain letters, numbers and spaces."
        )
