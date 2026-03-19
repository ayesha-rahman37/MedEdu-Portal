from django.db import models
from django.contrib.auth.models import AbstractUser
import random


class User(AbstractUser):

    ROLE_CHOICES = (
        ('medical_student', 'Medical Student'),
        ('dental_student', 'Dental Student'),
        ('intern', 'Intern Doctor'),
        ('faculty', 'Faculty'),
        ('doctor', 'Doctor'),
        ('ward', 'Ward Authority'),
        ('library', 'Library Staff'),
        ('admin', 'Admin'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    mededu_id = models.CharField(max_length=20, unique=True, blank=True)

    phone = models.CharField(max_length=15, blank=True)

    is_verified = models.BooleanField(default=False)

    profile_pic = models.ImageField(upload_to="profile/", null=True, blank=True)


    # ================= ID GENERATOR =================
    def generate_id(self):

        prefix_map = {
            "medical_student": "MS",
            "dental_student": "DS",
            "intern": "IN",
            "faculty": "FA",
            "doctor": "DR",
            "ward": "WA",
            "library": "LB",
            "admin": "AD"
        }

        prefix = prefix_map.get(self.role, "US")

        # 🔥 ensure unique ID
        while True:
            number = random.randint(1000, 9999)
            new_id = f"{prefix}-{number}"

            if not User.objects.filter(mededu_id=new_id).exists():
                return new_id


    # ================= SAVE =================
    def save(self, *args, **kwargs):

        if not self.mededu_id:
            self.mededu_id = self.generate_id()

        super().save(*args, **kwargs)