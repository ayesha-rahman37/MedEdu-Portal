from django.db import models
from django.utils.text import slugify
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


# ================= SUBJECT =================
class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    phase = models.IntegerField()
    course_type = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name

    
# ================= TOPIC (SYLLABUS) =================
class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.TextField()
    full_marks = models.IntegerField(default=10)

    def __str__(self):
        return self.title


# ================= EXAM ROUTINE =================
class ExamSchedule(models.Model):
    EXAM_TYPE = (
        ("item", "Item"),
        ("card", "Card"),
        ("term", "Term"),
    )

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE)
    date = models.DateField()

    def __str__(self):
        return f"{self.subject.name} - {self.exam_type}"


# ================= RESULT =================
class Result(models.Model):

    STATUS = (
        ("pending", "Pending"),
        ("clear", "Clear"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    marks = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.topic.title}"