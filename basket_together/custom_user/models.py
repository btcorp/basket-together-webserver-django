from django.db import models
# from time import timezone
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# from django.core.mail from send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _

'''
class CustomUserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves User with the given email and password.
        """
        now = timezone.now()
        
        if not email:
            raise ValueError('The given email must be set.')
        
        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff, is_active=True,
            is_superuser=is_superuser, last_login=now,
            date_joined=now, **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

   
class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=254, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=254, blank=True)
    phone_number = models.CharField(max_length=12)
    device_type = models.CharField(max_length=1, default='a')
    join_path = models.CharField(max_length=20, default='general')
    attend_count = models.IntegerField(blank=True)
    penalty_count = models.IntegerField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)


    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
'''
