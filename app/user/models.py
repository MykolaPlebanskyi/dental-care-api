"""
Database models for the user application.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for User model."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """Create and return a superuser with given details."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    class ROLES(models.TextChoices):
        ADMIN = 'admin', 'Адміністратор'
        DENTIST = 'dentist', 'Стоматолог'
        PATIENT = 'patient', 'Пацієнт'
        GUEST = 'guest', 'Гість'

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLES.choices, default=ROLES.GUEST)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    must_change_password = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.email})'

class Dentist(models.Model):
    """Dentist profile model with specialization and biography."""

    SPECIALIZATIONS = [
        ('therapist', 'Терапевт'),
        ('surgeon', 'Хірург'),
        ('orthodontist', 'Ортодонт'),
        ('prosthodontist', 'Ортопед'),
        ('periodontist', 'Пародонтолог'),
        ('endodontist', 'Ендодонтист'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dentist_profile'
    )
    specialization = models.CharField(max_length=30, choices=SPECIALIZATIONS)
    biography = models.TextField(blank=True)
    photo = models.ImageField(upload_to='dentist_photos/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} - {self.get_specialization_display()}'