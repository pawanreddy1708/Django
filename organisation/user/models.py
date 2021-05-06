from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self,email,username,phone,password=None):
        if username is None:
            raise TypeError('user should have a username')
        if email is None:
            raise TypeError('user should have a mail ID')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            phone=phone
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password=None):
        
        if password is None:
            raise TypeError("Password for super user cannot be empty")

        user = self.create_user(email,username,password)
        user.is_superuser=True
        user.is_staff =True
        user.is_active = True
        user.is_verified =True
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    username=models.CharField(max_length=255,unique=True,db_index=True)
    email = models.CharField(max_length=255,unique=True,db_index=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff=models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.BigIntegerField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def get_email(self):
        return self.email

    def __str__(self):
        return self.email
    