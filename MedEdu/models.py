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

        # ensure unique ID
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
    CATEGORY_CHOICES = [
        ('textbook', 'Textbook'),
        ('reference', 'Reference'),
        ('journal', 'Journal'),
        ('general', 'General Reading'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='textbook')
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
            fine = days_overdue * 5  # 5 টাকা per day
            self.fine_amount = fine
            self.status = 'overdue'
            self.save(update_fields=['fine_amount', 'status'])
        return self.fine_amount
    
    def get_days_overdue(self):
        """Get number of days overdue"""
        from django.utils import timezone
        if self.status in ['issued', 'overdue'] and timezone.now().date() > self.due_date:
            return (timezone.now().date() - self.due_date).days
        return 0
    
    def get_days_remaining(self):
        """Get number of days remaining until due date"""
        from django.utils import timezone
        if self.status in ['issued', 'overdue'] and timezone.now().date() <= self.due_date:
            return (self.due_date - timezone.now().date()).days
        return 0
    
    def is_overdue(self):
        """Check if book is overdue"""
        from django.utils import timezone
        return self.status in ['issued', 'overdue'] and timezone.now().date() > self.due_date


class BookReservation(models.Model):
    """Book reservation system"""
    RESERVATION_STATUS = [
        ('active', 'Active'),
        ('fulfilled', 'Fulfilled'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=RESERVATION_STATUS, default='active')
    
    def __str__(self):
        return f"{self.book.title} reserved by {self.user.username}"
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expiry_date
    # ================= WARD POSTING MANAGEMENT =================

class Ward(models.Model):
    """Ward information"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    floor = models.CharField(max_length=20, blank=True)
    capacity = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class WardPosting(models.Model):
    """Ward posting schedule for students"""
    
    POSTING_TYPE = (
        ('morning', 'Morning Shift (8 AM - 2 PM)'),
        ('evening', 'Evening Shift (2 PM - 8 PM)'),
        ('night', 'Night Shift (8 PM - 8 AM)'),
        ('full_day', 'Full Day (8 AM - 8 PM)'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ward_postings', limit_choices_to={'role__in': ['medical_student', 'dental_student', 'intern']})
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='postings')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_postings', limit_choices_to={'role__in': ['doctor', 'faculty']})
    
    posting_type = models.CharField(max_length=20, choices=POSTING_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.ward.name} ({self.start_date} to {self.end_date})"
    
    def get_duration_days(self):
        return (self.end_date - self.start_date).days + 1
    
    def is_active(self):
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date and self.status == 'scheduled'
    
    def get_current_shift(self):
        from django.utils import timezone
        now = timezone.now()
        if self.start_date <= now.date() <= self.end_date:
            if self.posting_type == 'morning':
                return "Morning Shift (8 AM - 2 PM)"
            elif self.posting_type == 'evening':
                return "Evening Shift (2 PM - 8 PM)"
            elif self.posting_type == 'night':
                return "Night Shift (8 PM - 8 AM)"
            else:
                return "Full Day (8 AM - 8 PM)"
        return "Not Active"


class WardAttendance(models.Model):
    """Attendance for ward posting"""
    ATTENDANCE_STATUS = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('half_day', 'Half Day'),
        ('leave', 'On Leave'),
    )
    
    posting = models.ForeignKey(WardPosting, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS, default='present')
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='marked_attendances')
    
    class Meta:
        unique_together = ['posting', 'date']
    
    def __str__(self):
        return f"{self.posting.student.username} - {self.date} - {self.status}"