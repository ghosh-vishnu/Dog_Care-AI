from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.pets.models import Pet


class Vaccination(models.Model):
    """
    Vaccination records for pets.
    Linked to Pet model with vaccine name, due date, and status.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue'),
        ('scheduled', 'Scheduled'),
    ]

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccinations',
        db_index=True
    )
    vaccine_name = models.CharField(
        max_length=200,
        db_index=True,
        help_text='Name of the vaccine (e.g., Rabies, DHPP, etc.)'
    )
    due_date = models.DateField(
        db_index=True,
        help_text='Due date for the vaccination'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    administered_date = models.DateField(
        blank=True,
        null=True,
        help_text='Date when vaccine was actually administered'
    )
    veterinarian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='administered_vaccinations',
        limit_choices_to={'is_veterinarian': True},
        help_text='Veterinarian who administered the vaccine'
    )
    batch_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Batch number of the vaccine'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Additional notes about the vaccination'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vaccinations'
        verbose_name = 'Vaccination'
        verbose_name_plural = 'Vaccinations'
        ordering = ['-due_date', '-created_at']
        indexes = [
            models.Index(fields=['pet', 'status']),
            models.Index(fields=['due_date', 'status']),
        ]

    def __str__(self):
        return f"{self.pet.name} - {self.vaccine_name} ({self.get_status_display()})"

    def clean(self):
        """
        Validate vaccination data.
        """
        from django.core.exceptions import ValidationError
        
        if self.administered_date and self.due_date:
            if self.administered_date > timezone.now().date():
                raise ValidationError({
                    'administered_date': 'Administered date cannot be in the future.'
                })
        
        if self.status == 'completed' and not self.administered_date:
            raise ValidationError({
                'administered_date': 'Administered date is required for completed vaccinations.'
            })

    def save(self, *args, **kwargs):
        """
        Override save to update status based on due_date.
        """
        self.full_clean()
        
        if self.due_date and not self.administered_date:
            today = timezone.now().date()
            if self.due_date < today and self.status != 'completed':
                self.status = 'overdue'
            elif self.due_date >= today and self.status == 'overdue':
                self.status = 'pending'
        
        if self.administered_date:
            self.status = 'completed'
        
        super().save(*args, **kwargs)


class HealthRecord(models.Model):
    """
    Basic health records for pets.
    Linked to Pet model with weight, notes, and record date.
    """
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='health_records',
        db_index=True
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01, message='Weight must be greater than 0.'),
            MaxValueValidator(500.0, message='Weight cannot exceed 500 kg.')
        ],
        help_text='Weight of the pet in kg'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Health notes and observations'
    )
    record_date = models.DateField(
        db_index=True,
        help_text='Date of the health record'
    )
    veterinarian = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='health_record_entries',
        limit_choices_to={'is_veterinarian': True},
        help_text='Veterinarian who created this record'
    )
    temperature = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(30.0, message='Temperature must be at least 30°C.'),
            MaxValueValidator(45.0, message='Temperature cannot exceed 45°C.')
        ],
        help_text='Body temperature in Celsius'
    )
    heart_rate = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(40, message='Heart rate must be at least 40 bpm.'),
            MaxValueValidator(300, message='Heart rate cannot exceed 300 bpm.')
        ],
        help_text='Heart rate in beats per minute'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'health_records'
        verbose_name = 'Health Record'
        verbose_name_plural = 'Health Records'
        ordering = ['-record_date', '-created_at']
        indexes = [
            models.Index(fields=['pet', 'record_date']),
            models.Index(fields=['record_date']),
        ]

    def __str__(self):
        return f"{self.pet.name} - {self.record_date} ({self.weight} kg)"

    def clean(self):
        """
        Validate health record data.
        """
        from django.core.exceptions import ValidationError
        
        if self.record_date:
            today = timezone.now().date()
            if self.record_date > today:
                raise ValidationError({
                    'record_date': 'Record date cannot be in the future.'
                })

    def save(self, *args, **kwargs):
        """
        Override save to run validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)
