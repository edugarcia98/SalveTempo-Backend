from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Usuários devem possuir e-mail.")
        if not username:
            raise ValueError("Usuários devem possuir username.")
        if not password:
            raise ValueError("Usuários devem possuir senha.")

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            password = password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            username = username
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, verbose_name="E-mail")
    username = models.CharField(max_length=30, verbose_name="Usuário")
    date_joined = models.DateTimeField(verbose_name="Data de Entrada", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Último Login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True