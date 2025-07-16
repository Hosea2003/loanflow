from django.db import models

from users.models import Account, AppUser

class Beneficiary(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE
    )
    iban = models.CharField(max_length=50, null=False, blank=False)
    name = models.CharField(max_length=150)

class TransactionStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    COMPLETED = "COMPLETED", "Completed"
    FAILED = "FAILED", "Failed"

class Transaction(models.Model):
    sender = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        default=0
    )
    note = models.CharField(
        max_length=300
    )

    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return super().__str__()