from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
import random
from django.conf import settings


# ================= USER =================
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

    # ===== ID GENERATOR =====
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

        while True:
            number = random.randint(1000, 9999)
            new_id = f"{prefix}-{number}"

            if not User.objects.filter(mededu_id=new_id).exists():
                return new_id

    # ===== SAVE =====
    def save(self, *args, **kwargs):
        if not self.mededu_id:
            self.mededu_id = self.generate_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


# ================= SUBJECT =================
class Subject(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    phase = models.IntegerField()
    course_type = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ================= TOPIC =================
class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.TextField()
    full_marks = models.IntegerField(default=10)

    def __str__(self):
        return self.title


# ================= EXAM =================
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

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    marks = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    date = models.DateField(null=True, blank=True)

# ================= DOCTOR SCHEDULE =================
class DoctorSchedule(models.Model):

    DUTY_CHOICES = (
        ("ward", "Ward Round"),
        ("ot", "Operation"),
        ("lecture", "Lecture"),
        ("opd", "OPD"),
    )

    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    duty_type = models.CharField(max_length=20, choices=DUTY_CHOICES)

    title = models.CharField(max_length=200)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.doctor} - {self.duty_type}"


# ================= LIBRARY =================
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)

    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class Issue(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    
    returned = models.BooleanField(default=False)
    
    fine = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.student} - {self.book}"
    
# ================= EXAM NOTICE =================
class ExamNotice(models.Model):

    EXAM_TYPE = (
        ("card", "Card"),
        ("term", "Term"),
    )

    COURSE_TYPE = (
        ("MBBS", "MBBS"),
        ("BDS", "BDS"),
    )

    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE)
    course = models.CharField(max_length=10, choices=COURSE_TYPE)
    phase = models.IntegerField()

    title = models.CharField(max_length=200)
    description = models.TextField()

    date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.exam_type} - Phase {self.phase}"
    
    
# ================= PAYMENT =================
class Payment(models.Model):

    METHOD_CHOICES = (
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('bank', 'Bank'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    amount = models.IntegerField()
    method = models.CharField(max_length=10, choices=METHOD_CHOICES)

    bank_name = models.CharField(max_length=100, blank=True, null=True)

    purpose = models.CharField(max_length=200)  # 🔥 user লিখবে

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount}"


# ================= STUDENT DUE =================
class StudentDue(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_due = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - Due: {self.total_due}"


# ================= SALARY =================
class Salary(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    amount = models.IntegerField()
    month = models.CharField(max_length=20)

    bank_name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return f"{self.user} - {self.month}"
    

# ================= STUDENT ACADEMIC RECORD =================
class StudentRecord(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    attendance = models.IntegerField(default=0)

    item_pass = models.BooleanField(default=False)
    card_pass = models.BooleanField(default=False)
    term_pass = models.BooleanField(default=False)

    payment_clear = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# ================= FACULTY CLASS SCHEDULE =================
class ClassSchedule(models.Model):

    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    year = models.CharField(max_length=50)   # e.g. 1st Year
    subject = models.CharField(max_length=100)

    room = models.CharField(max_length=100)

    date = models.DateField()

    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.faculty} - {self.subject} ({self.date})"
    
class Attendance(models.Model):
    
    STATUS = (
        ("present", "Present"),
        ("absent", "Absent"),
    )

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS)

    def __str__(self):
        return f"{self.student} - {self.status}"