from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
import string
from django.core.exceptions import ValidationError

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

def generate_iban(country_code="MG", bank_code="12345678", account_number_length=10):
    account_number = ''.join(random.choices(string.digits, k=account_number_length))
    bban = bank_code + account_number
    check_string = bban + country_code + "00"
    check_string = ''.join(str(ord(c) - 55) if c.isalpha() else c for c in check_string.upper())
    check_num = int(check_string)
    check_digits = 98 - (check_num % 97)
    check_digits = f"{check_digits:02d}"
    iban = f"{country_code}{check_digits}{bban}"
    return iban

def validate_iban(iban):
    """
    Validate an IBAN number.
    
    Args:
        iban (str): IBAN to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    iban = iban.replace(" ", "").upper()
    
    if len(iban) < 15 or len(iban) > 34:
        return False
    
    if not iban[:2].isalpha() or not iban[2:4].isdigit():
        return False
    
    check_string = iban[4:] + iban[:4]
    check_string = ''.join(str(int(c) + 10 if c.isalpha() else c) for c in check_string)
    
    return int(check_string) % 97 == 1


class Account(models.Model):
    owner = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='accounts'
    )
    iban = models.CharField(max_length=50, null=False, blank=False)
    balance = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        default=0
    )
    # for easier reading
    name = models.CharField(max_length=150, null=True, blank=True)

    def clean(self):
        if not self.iban and not validate_iban(self.iban):
            ValidationError({"iban":"invalid format"})
        return super().clean()

    def save(self, **kwargs):
        # on create, generate iban
        if not self.pk:
            self.iban = generate_iban()
        return super().save(**kwargs)