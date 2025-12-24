from django.db import models
from django.conf import settings
from apps.pets.models import Pet


class Appointment(models.Model):
    """
    Appointment model for scheduling vet visits.
    """
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    veterinarian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='vet_appointments',
        limit_choices_to={'is_veterinarian': True}
    )
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-appointment_date']
        indexes = [
            models.Index(fields=['owner', 'status']),
            models.Index(fields=['pet', 'appointment_date']),
            models.Index(fields=['appointment_date', 'status']),
            models.Index(fields=['veterinarian', 'appointment_date']),
        ]

    def __str__(self):
        return f"{self.pet.name} - {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        """
        Validate appointment data.
        """
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        if self.appointment_date:
            if self.appointment_date < timezone.now():
                raise ValidationError({
                    'appointment_date': 'Appointment date cannot be in the past.'
                })
        
        if self.pet and self.owner:
            if self.pet.owner != self.owner:
                raise ValidationError({
                    'pet': 'Pet must belong to the specified owner.'
                })

    def save(self, *args, **kwargs):
        """
        Override save to run validation and set owner from pet if not provided.
        """
        if not self.owner and self.pet:
            self.owner = self.pet.owner
        self.full_clean()
        super().save(*args, **kwargs)
