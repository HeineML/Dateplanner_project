from django.db import models
from django.contrib.auth.models import User


class Unavailability(models.Model):
    """Datoer Heine legger inn som IKKE tilgjengelig."""
    date = models.DateField(unique=True)
    note = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"Utilgjengelig {self.date}"


class DateRequest(models.Model):
    """En date-forespørsel Linnea sender inn."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Venter'
        CONFIRMED = 'confirmed', 'Bekreftet'
        DECLINED = 'declined', 'Avslått'

    date = models.DateField()
    activity = models.CharField(max_length=100, blank=True)
    message = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='date_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.date} ({self.get_status_display()})"
