def can_view_all_gifthospitality(user):
    """Checks view permission, if the user can view gifthospitality
    they are allowed to view the section"""

    if user.is_superuser:
        return True

    return user.has_perm(
        "gifthospitality.can_view_all_gifthospitality"
    )


def user_in_group(user, group):
    return user.groups.filter(
        name=group,
    ).exists()
