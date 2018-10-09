from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """if you wanted to over-ride behaviour of createsuperuser and, createuser commands,
    you would do it here!
    However, we don't want to use this feature at all, thus we have created commands. 
    these commands are locaated at management/commands which prints text 'command is disabled'
    """
    pass
