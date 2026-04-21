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

# ================= DOCTOR SCHEDULE =================

class DoctorSchedule(models.Model):

    DUTY_CHOICES = (
        ("ward", "Ward Round"),
        ("ot", "Operation"),
        ("lecture", "Lecture"),
        ("opd", "OPD"),
    )

    doctor = models.ForeignKey(User, on_delete=models.CASCADE)
    duty_type = models.CharField(max_length=20, choices=DUTY_CHOICES)

    title = models.CharField(max_length=200)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.doctor.mededu_id} - {self.duty_type}"
    # ================= LIBRARY MANAGEMENT =================

class Book(models.Model):
    """Book model for library management"""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('textbook', 'Textbook'),
        ('reference', 'Reference'),
        ('journal', 'Journal'),
        ('general', 'General Reading'),
    ], default='textbook')
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    location = models.CharField(max_length=100, blank=True, help_text="Rack/Shelf location")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if not self.isbn:
            import random
            self.isbn = f"{random.randint(1000000000000, 9999999999999)}"
        super().save(*args, **kwargs)


class BookIssue(models.Model):
    """Track book issues to users"""
    STATUS_CHOICES = (
        ('issued', 'Issued'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_issues')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='issues')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='issued')
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    fine_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.book.title} issued to {self.user.username}"
    
    def calculate_fine(self):
        """Calculate fine if book is overdue"""
        from django.utils import timezone
        if self.status == 'issued' and timezone.now().date() > self.due_date:
            days_overdue = (timezone.now().date() - self.due_date).days
            # Fine rate: 5 taka per day
            fine = days_overdue * 5
            self.fine_amount = fine
            self.status = 'overdue'
            self.save()
        return self.fine_amount


class BookReservation(models.Model):
    """Book reservation system"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], default='active')
    
    def __str__(self):
        return f"{self.book.title} reserved by {self.user.username}"