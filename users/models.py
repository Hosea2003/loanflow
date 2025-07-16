from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class AppUserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **kwargs):
        if not email and not username:
            raise ValueError("email or username should be included  ")

        self.normalize_email(email=email)

        user = self.model(
            email=email,
            username=username,
            **kwargs
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("role", "CONSULTANT")

        return self.create_user(username, email, password=password, **kwargs)

class AppUser(AbstractUser):

    email = models.EmailField(unique=True, null=False, blank=False)
    phone = models.CharField(max_length=20)
    
    class AppUserRoles(models.TextChoices):
        CLIENT="CLIENT", _("Client"),
        CONSULTANT="CONSULTANT", _("Consultant")
    role = models.CharField(
        max_length=30,
        choices=AppUserRoles.choices,
        default=AppUserRoles.CLIENT
    )

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = [
        'email',
        'first_name',
        'last_name'
    ]

    objects = AppUserManager()

    class Meta:
        verbose_name = "Loanflow User"