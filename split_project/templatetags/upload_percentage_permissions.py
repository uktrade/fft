from django import template

register = template.Library()


@register.simple_tag
def has_project_percentage_permission(user):
    if user.is_superuser:
        return True
    elif user.has_perm(
        "split_project.can_upload_percentage_files"
    ) or user.groups.filter(
        name="Project Split Administrator"
    ):
        return True
    else:
        return False
