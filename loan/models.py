from django.db import models
from users.models import AppUser

class LoanStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    ACCEPTED = "ACCEPTED", "Accepted"
    DENIED = "DENIED", "Denied"

class Loan(models.Model):
    user = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='loans'
    )
    consultant = models.ForeignKey(
        AppUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="loans_to_consult"
    )
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=LoanStatus.choices,
        default=LoanStatus.PENDING
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_assigned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Loan #{self.pk} - {self.amount} ({self.status})"