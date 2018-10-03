from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def _create_user(self,email,password,is_active,is_staff,is_superuser,**extra_fields):
        if not email:
            raise ValueError('an Email address is required')

        if 'username' in extra_fields:
            raise ValueError('username should not be present, use email address for username field')
        
        user = self.model(  email=self.normalize_email(email),
                            is_active=is_active,
                            is_staff=is_staff,
                            is_superuser=is_superuser,
                            **extra_fields)

        user.set_unusable_password  (password)
        user.save(using=self._db)
        return user

    #Disabled Command line user creation
    #This is to ensure, user is entered strictly via SSO auth
    def create_user(self,email=None,password=None,**extra_fields):
        # extra_fields.setdefault('is_active',True)
        # extra_fields.setdefault('is_staff',False)
        # extra_fields.setdefault('is_superuser',False)
        # return self._create_user(email,password,**extra_fields)
        return None

    #Disabled Commad line superuser creation
    #This is to ensure, user is entered strictly via SSO auth
    def create_superuser(self,email,password,**extra_fields):
        # extra_fields.setdefault('is_active',True)
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError('Superuser must have is_staff=True.')
        # if extra_fields.get('is_superuser') is not True:
        #     raise ValueError('Superuser must have is_superuser=True.')
        # return self._create_user(email,password,**extra_fields)
        return None
