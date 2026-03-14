from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):

    ROLE_CHOICES = (
        ('student', 'Medical & Dental Student'),
        ('intern', 'Intern Doctor'),
        ('faculty', 'Faculty / Department Head'),
        ('doctor', 'Doctor'),
        ('ward', 'Hospital Register'),
        ('library', 'Library Staff'),
        ('admin', 'Academic Administration'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    mededu_id = models.CharField(max_length=20, unique=True, blank=True)

    phone = models.CharField(max_length=15, blank=True)


    def generate_id(self):

        prefix_map = {
            "student": "ST",
            "intern": "IN",
            "faculty": "FA",
            "doctor": "DR",
            "ward": "WA",
            "library": "LB",
            "admin": "AD"
        }

        prefix = prefix_map.get(self.role)

        number = random.randint(1000, 9999)

        return f"{prefix}-{number}"


    def save(self, *args, **kwargs):

        if not self.mededu_id:
            self.mededu_id = self.generate_id()

        super().save(*args, **kwargs)
