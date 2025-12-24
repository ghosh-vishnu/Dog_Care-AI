from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class PetManager(models.Manager):
    """
    Custom manager for Pet model with soft delete support.
    """
    def get_queryset(self):
        """
        Return only non-deleted pets by default.
        """
        return super().get_queryset().filter(is_deleted=False)

    def all_with_deleted(self):
        """
        Return all pets including deleted ones.
        """
        return super().get_queryset()

    def deleted_only(self):
        """
        Return only deleted pets.
        """
        return super().get_queryset().filter(is_deleted=True)


class Pet(models.Model):
    """
    Pet model to store pet information with soft delete support.
    One user can have multiple pets.
    """
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('unknown', 'Unknown'),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets',
        db_index=True,
        help_text='User who owns this pet'
    )
    name = models.CharField(
        max_length=100,
        help_text='Pet name'
    )
    breed = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Pet breed'
    )
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(50)
        ],
        help_text='Pet age in years'
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000)
        ],
        help_text='Pet weight in kg'
    )
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='unknown',
        help_text='Pet gender'
    )
    pet_type = models.CharField(
        max_length=20,
        choices=PET_TYPES,
        default='dog',
        db_index=True,
        help_text='Type of pet'
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        help_text='Pet date of birth'
    )
    color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text='Pet color/markings'
    )
    profile_picture = models.ImageField(
        upload_to='pets/',
        blank=True,
        null=True,
        help_text='Pet profile picture'
    )
    microchip_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        db_index=True,
        help_text='Microchip identification number'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Additional notes about the pet'
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text='Soft delete flag'
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Timestamp when pet was deleted'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PetManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'pets'
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['owner', 'is_deleted']),
            models.Index(fields=['pet_type', 'is_deleted']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_pet_type_display()})"

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete implementation.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using)

    def restore(self):
        """
        Restore a soft-deleted pet.
        """
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        """
        Permanently delete the pet from database.
        """
        super().delete()

    def clean(self):
        """
        Validate model fields.
        """
        super().clean()
        if self.microchip_number:
            self.microchip_number = self.microchip_number.strip().upper()

    def save(self, *args, **kwargs):
        """
        Override save to ensure validation and calculate age if date_of_birth is provided.
        """
        self.full_clean()
        if self.date_of_birth and not self.age:
            today = timezone.now().date()
            self.age = (today - self.date_of_birth).days // 365
        super().save(*args, **kwargs)
