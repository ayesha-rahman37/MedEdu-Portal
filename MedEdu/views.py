from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.contrib import messages
from .models import User, Subject, Topic, ExamSchedule, Result, DoctorSchedule, Book, BookIssue, BookReservation, Ward, WardPosting, WardAttendance
from datetime import date, timedelta
from django.utils import timezone
# ================= HOME =================
def home(request):
    return render(request, "home.html")


# ================= SIGNUP =================
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        password = request.POST.get("password")

        # duplicate check
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already exists"})

        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {"error": "Email already exists"})

        user = User.objects.create(
            username=username,
            email=email,
            phone=phone,
            role=role,
            is_verified=False
        )

        user.set_password(password)

        # ===== MedEdu ID =====
        if role == "medical_student":
            prefix = "MS"
        elif role == "dental_student":
            prefix = "DS"
        elif role == "faculty":
            prefix = "F"
        elif role == "intern":
            prefix = "I"
        elif role == "doctor":
            prefix = "D"
        elif role == "ward":
            prefix = "W"
        elif role == "library":
            prefix = "L"
        else:
            prefix = "A"

        number = User.objects.count() + 1000
        user.mededu_id = f"{prefix}-{number}"

        user.save()

        # ===== EMAIL VERIFY =====
        link = request.build_absolute_uri(
            reverse("verify_account", args=[user.id])
        )

        send_mail(
            "Verify Your Account",
            f"Click to verify: {link}",
            settings.EMAIL_HOST_USER,
            [email],
        )

        return render(request, "signup_success.html", {"mededu_id": user.mededu_id})

    return render(request, "signup.html")


# ================= VERIFY =================
def verify_account(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_verified = True
        user.save()
    except:
        pass

    return redirect("login")


# ================= LOGIN =================
def login_view(request):

    if request.method == "POST":

        mededu_id = request.POST.get("mededu_id")
        password = request.POST.get("password")

        try:
            user = User.objects.get(mededu_id=mededu_id)

            if not user.is_verified:
                return render(request, "login.html", {
                    "error": "Please verify your account first"
                })

            if user.check_password(password):
                login(request, user)
                return redirect("dashboard")
            else:
                return render(request, "login.html", {
                    "error": "Invalid password"
                })

        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "User not found"
            })

    return render(request, "login.html")


# ================= LOGOUT =================
def logout_view(request):
    logout(request)
    return redirect("home")


# ================= RESET PASSWORD =================
def forgot_password(request):

    if request.method == "POST":

        mededu_id = request.POST.get("mededu_id")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not mededu_id or not new_password or not confirm_password:
            return render(request, "reset.html", {"error": "All fields required"})

        if new_password != confirm_password:
            return render(request, "reset.html", {"error": "Passwords do not match"})

        try:
            user = User.objects.get(mededu_id=mededu_id)

            user.set_password(new_password)
            user.save()

            return render(request, "reset.html", {"success": "Password updated!"})

        except User.DoesNotExist:
            return render(request, "reset.html", {"error": "Invalid ID"})

    return render(request, "reset.html")


# ================= PROFILE =================
@login_required
def profile_view(request):
    return render(request, "profile.html")


# ================= EDIT PROFILE =================
@login_required
def edit_profile(request):

    if request.method == "POST":

        if request.FILES.get("profile_pic"):
            request.user.profile_pic = request.FILES.get("profile_pic")

        request.user.save()
        return redirect("profile")

    return render(request, "update_profile.html")


# ================= DASHBOARD REDIRECT =================
@login_required
def dashboard_redirect(request):

    role = request.user.role

    if role in ["medical_student", "dental_student"]:
        return redirect("student_dashboard")

    elif role == "faculty":
        return redirect("faculty_dashboard")

    elif role == "intern":
        return redirect("intern_dashboard")

    elif role == "doctor":
        return redirect("doctor_dashboard")

    elif role == "ward":
        return redirect("ward_dashboard")

    elif role == "library":
        return redirect("library_dashboard")

    elif role == "admin":
        return redirect("admin_dashboard")

    return redirect("home")


# ================= DASHBOARDS =================
@login_required
def student_dashboard(request):
    role = request.user.role.replace("_", " ").title()
    return render(request, "dashboards/student_dashboard.html", {"role": role})


@login_required
def faculty_dashboard(request):
    role = request.user.role.replace("_", " ").title()
    return render(request, "dashboards/faculty_dashboard.html", {"role": role})


@login_required
def intern_dashboard(request):
    role = request.user.role.replace("_", " ").title()
    return render(request, "dashboards/intern_dashboard.html", {"role": role})


@login_required
def doctor_dashboard(request):
    role = request.user.role.replace("_", " ").title()
    return render(request, "dashboards/doctor_dashboard.html", {"role": role})


@login_required
def ward_dashboard(request):
    role = request.user.role.replace("_", " ").title()
    return render(request, "dashboards/ward_dashboard.html", {"role": role})


@login_required
def admin_dashboard(request):
    role = request.user.role.replace("_", " ").title()
    return render(request, "dashboards/admin_dashboard.html", {"role": role})


# ================= LIBRARY DASHBOARD =================
@login_required
def library_dashboard(request):
    """Library staff dashboard with statistics"""
    
    if request.user.role not in ['library', 'admin']:
        return redirect('dashboard')
    
    today = timezone.now().date()
    
    # Statistics
    total_books = Book.objects.count()
    available_books = Book.objects.aggregate(total=models.Sum('available_copies'))['total'] or 0
    total_issued = BookIssue.objects.filter(status='issued').count()
    total_overdue = BookIssue.objects.filter(status='overdue').count()
    
    # Due date statistics
    due_today = BookIssue.objects.filter(due_date=today, status='issued').count()
    due_this_week = BookIssue.objects.filter(
        due_date__gte=today,
        due_date__lte=today + timedelta(days=7),
        status='issued'
    ).count()
    
    # Recently issued books with due date info
    recent_issues = BookIssue.objects.select_related('user', 'book').order_by('-issue_date')[:10]
    
    # Add due date info to each issue
    for issue in recent_issues:
        issue.days_overdue = issue.get_days_overdue()
        issue.days_remaining = issue.get_days_remaining()
        issue.is_overdue = issue.is_overdue()
    
    # Books with low stock
    low_stock_books = Book.objects.filter(available_copies__lte=2, available_copies__gt=0)
    
    # Overdue books list (for alert)
    overdue_books = BookIssue.objects.filter(
        status='overdue'
    ).select_related('user', 'book')[:10]
    
    # Add days overdue to each overdue book
    for issue in overdue_books:
        issue.days_overdue = issue.get_days_overdue()
    
    context = {
        'total_books': total_books,
        'available_books': available_books,
        'total_issued': total_issued,
        'total_overdue': total_overdue,
        'due_today': due_today,
        'due_this_week': due_this_week,
        'recent_issues': recent_issues,
        'low_stock_books': low_stock_books,
        'overdue_books': overdue_books,
        'today': today,
    }
    
    return render(request, 'library/dashboard.html', context)


# ================= SUBJECT =================
@login_required
def subject_list(request):

    if request.user.role == "medical_student":
        subjects = Subject.objects.filter(course_type="medical")

    elif request.user.role == "dental_student":
        subjects = Subject.objects.filter(course_type="dental")

    else:
        subjects = Subject.objects.all()

    return render(request, "subjects.html", {
        "subjects": subjects
    })


# ================= SUBJECT DETAIL =================

@login_required
def subject_detail(request, slug):
    # ONLY STUDENTS CAN ACCESS
    if request.user.role not in ["medical_student", "dental_student"]:
        return redirect("dashboard")

    subject = get_object_or_404(Subject, slug=slug)
    topics = Topic.objects.filter(subject=subject)

    user = request.user
    course = None
    # course detect (IMPORTANT - uppercase folder match)
    if user.role == "medical_student":
        course = "MBBS"
    elif user.role == "dental_student":
        course = "BDS"

    # EXACT PDF PATH (your real files)
    pdf_map = {

        # medical subjects
        # phase 1
        "anatomy": f"/static/pdfs/{course}/Phase 1/Anatomy.pdf",
        "physiology": f"/static/pdfs/{course}/Phase 1/Physiology.pdf",
        "biochemistry": f"/static/pdfs/{course}/Phase 1/Biochemistry.pdf",

        # phase 2
        "pharmacology-therapeutics": f"/static/pdfs/{course}/Phase 2/Pharmacology & Therapeutics.pdf",
        "forensic-medicine-toxicology": f"/static/pdfs/{course}/Phase 2/Forensic Medicine & Toxicology.pdf",
        "general-pathology-basic": f"/static/pdfs/{course}/Phase 3/Pathology.pdf",
        "general-microbiology-basic": f"/static/pdfs/{course}/Phase 3/Microbiology.pdf",
        "medicine-intro": f"/static/pdfs/{course}/Phase 4/Medicine.pdf",
        "surgery-intro": f"/static/pdfs/{course}/Phase 4/Surgery & Allied Subjects.pdf",

        # phase 3
        "community-medicine-public-health": f"/static/pdfs/{course}/Phase 3/Community Medicine & Public Health.pdf",
        "pathology": f"/static/pdfs/{course}/Phase 3/Pathology.pdf",
        "microbiology": f"/static/pdfs/{course}/Phase 3/Microbiology.pdf",
        "medicine-clinical": f"/static/pdfs/{course}/Phase 4/Medicine.pdf",
        "surgery-clinical": f"/static/pdfs/{course}/Phase 4/Surgery & Allied Subjects.pdf",
        "obstetrics-gynaecology-intro": f"/static/pdfs/{course}/Phase 4/Obstetrics & Gynaecology.pdf",

        # phase 4
        "medicine": f"/static/pdfs/{course}/Phase 4/Medicine.pdf",
        "surgery": f"/static/pdfs/{course}/Phase 4/Surgery & Allied Subjects.pdf",
        "obstetrics-gynaecology": f"/static/pdfs/{course}/Phase 4/Obstetrics & Gynaecology.pdf",
        "extras": [
            f"/static/pdfs/{course}/Phase 4/Ophthalmology.pdf",
            f"/static/pdfs/{course}/Phase 4/Otorhinolaryngology & Head-Neck Surgery.pdf",
            f"/static/pdfs/{course}/Phase 4/Paediatrics.pdf",
            f"/static/pdfs/{course}/Phase 4/Psychiatry.pdf",
            f"/static/pdfs/{course}/Phase 4/Skin & VD.pdf",
        ],

        # dental subjects
        # phase 1
        "general-anatomy": f"/static/pdfs/{course}/Phase 1/Anatomy (Paper - I).pdf",
        "dental-anatomy": f"/static/pdfs/{course}/Phase 1/Dental Anatomy (Paper - II).pdf",
        "physiology-biochemistry": f"/static/pdfs/{course}/Phase 1/Physiology & Biochemistry.pdf",
        "science-of-dental-materials": f"/static/pdfs/{course}/Phase 1/Science of Dental Materials.pdf",

        # phase 2
        "general-pharmacology-dental-therapeutics": f"/static/pdfs/{course}/Phase 2/General Pharmacology & Dental Therapeutics.pdf",
        "pathology-microbiology": f"/static/pdfs/{course}/Phase 2/Pathology & Microbiology.pdf",

        # phase 3
        "medicine": f"/static/pdfs/{course}/Phase 3/Medicine.pdf",
        "surgery": f"/static/pdfs/{course}/Phase 3/Surgery.pdf",
        "periodontology-oral-pathology": f"/static/pdfs/{course}/Phase 3/Periodontology & Oral Pathology.pdf",

        # phase 4
        "oral-maxillofacial-surgery": f"/static/pdfs/{course}/Phase 4/Oral & Maxillofacial Surgery.pdf",
        "conservative-dentistry-endodontics": f"/static/pdfs/{course}/Phase 4/Conservative Dentistry & Endodontics.pdf",
        "prosthodontics": f"/static/pdfs/{course}/Phase 4/Prosthodontics.pdf",
        "orthodontics-dentofacial-orthopedics": f"/static/pdfs/{course}/Phase 4/Orthodontics & Dentofacial Orthopedics.pdf",
        "pedodontics-dental-public-health": f"/static/pdfs/{course}/Phase 4/Pedodontics & Dental Public Health.pdf",
        
    }

    data = pdf_map.get(slug)

    if isinstance(data, str):
        pdf_path = data
    
    elif isinstance(data, dict):
        pdf_path = data.get("main")
    
    else:
        pdf_path = None
    
    extra_pdfs = []

    phase4_subjects = [
        "medicine",
        "surgery",
        "obstetrics-gynaecology",
    ]

    if slug in phase4_subjects:
        extra_pdfs = pdf_map.get("extras", [])
    
    # Additional Resources (IT + Internship)

    if course == "MBBS":
        additional_resources = [
            {
                "name": "IT (Phase 1)",
                "file": f"/static/pdfs/{course}/Phase 1/IT Phase 1.pdf"
            },
            {
                "name": "IT (Phase 2)",
                "file": f"/static/pdfs/{course}/Phase 2/IT Phase 2.pdf"
            },
            {
                "name": "IT (Phase 3)",
                "file": f"/static/pdfs/{course}/Phase 3/IT Phase 3.pdf"
            },
            {
                "name": "IT (Phase 4)",
                "file": f"/static/pdfs/{course}/Phase 4/IT Phase 4.pdf"
            },
            {
                "name": "Internship",
                "file": f"/static/pdfs/{course}/Internship.pdf"
            },
            {
                "name": "Prescription",
                "file": f"/static/pdfs/{course}/Prescription.pdf"
            }
        ]
    

    elif course == "BDS":
        additional_resources = [
            {
                "name": "IT (Phase 1)",
                "file": f"/static/pdfs/{course}/Phase 1/IT Phase 1.pdf"
            },
            {
                "name": "Prescription",
                "file": f"/static/pdfs/{course}/Prescription.pdf"
            }
        ]
    
    return render(request, "subject_detail.html", {
        "subject": subject,
        "topics": topics,
        "pdf_path": pdf_path,
        "extra_pdfs": extra_pdfs,
        "additional_resources": additional_resources
    })


@login_required
def exam_page(request):

    # optional: filter based on student type
    if request.user.role == "medical_student":
        exams = ExamSchedule.objects.filter(subject__course_type="medical")

    elif request.user.role == "dental_student":
        exams = ExamSchedule.objects.filter(subject__course_type="dental")

    else:
        exams = ExamSchedule.objects.all()

    exams = exams.order_by("date")

    return render(request, "exam.html", {
        "exams": exams
    })


@login_required
def result_page(request):

    # ONLY own result
    results = Result.objects.filter(user=request.user)

    return render(request, "result.html", {
        "results": results
    })


# ================= DOCTOR SCHEDULE =================

@login_required
def doctor_schedule(request):

    # doctor না হলে block
    if request.user.role != "doctor":
        return render(request, "access_denied.html")

    # today's date
    today = date.today()

    # today's schedules
    today_schedules = DoctorSchedule.objects.filter(
        doctor=request.user,
        date=today
    ).order_by("start_time")

    # all schedules
    schedules = DoctorSchedule.objects.filter(
        doctor=request.user
    ).order_by("date", "start_time")

    # FINAL RETURN
    return render(request, "doctor_schedule.html", {
        "today_schedules": today_schedules,
        "schedules": schedules
    })


# ================= LIBRARY VIEWS =================

@login_required
def book_list(request):
    """Display all books with search and filter"""
    
    books = Book.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        books = books.filter(
            models.Q(title__icontains=search_query) |
            models.Q(author__icontains=search_query) |
            models.Q(isbn__icontains=search_query)
        )
    
    # Filter by category
    category = request.GET.get('category', '')
    if category:
        books = books.filter(category=category)
    
    # Filter by availability
    availability = request.GET.get('availability', '')
    if availability == 'available':
        books = books.filter(available_copies__gt=0)
    elif availability == 'unavailable':
        books = books.filter(available_copies=0)
    
    context = {
        'books': books,
        'search_query': search_query,
        'selected_category': category,
        'selected_availability': availability,
    }
    
    return render(request, 'library/book_list.html', context)


@login_required
def book_detail(request, book_id):
    """Display book details and issue history"""
    
    book = get_object_or_404(Book, id=book_id)
    
    # Get issue history for this book
    issue_history = BookIssue.objects.filter(book=book).select_related('user').order_by('-issue_date')[:20]
    
    # Get current reservations
    reservations = BookReservation.objects.filter(book=book, status='active')
    
    context = {
        'book': book,
        'issue_history': issue_history,
        'reservations': reservations,
    }
    
    return render(request, 'library/book_detail.html', context)


@login_required
def issue_book(request):
    """Issue a book to a user"""
    
    if request.user.role not in ['library', 'admin']:
        return redirect('dashboard')
    
    if request.method == 'POST':
        mededu_id = request.POST.get('mededu_id')
        book_title = request.POST.get('book_title')
        due_date_str = request.POST.get('due_date')
        
        try:
            user = User.objects.get(mededu_id=mededu_id)
            book = Book.objects.filter(title__icontains=book_title).first()
            
            if not book:
                messages.error(request, 'Book not found')
                return redirect('issue_book')
            
            if book.available_copies < 1:
                messages.error(request, 'No copies available for this book')
                return redirect('issue_book')
            
            due_date = date.fromisoformat(due_date_str)
            
            # Create issue record
            issue = BookIssue.objects.create(
                user=user,
                book=book,
                due_date=due_date,
                status='issued'
            )
            
            # Update available copies
            book.available_copies -= 1
            book.save()
            
            messages.success(request, f'Book "{book.title}" issued to {user.username}')
            return redirect('library_dashboard')
            
        except User.DoesNotExist:
            messages.error(request, 'User not found with this MedEdu ID')
            return redirect('issue_book')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('issue_book')
    
    return render(request, 'library/issue_book.html')


@login_required
def return_book(request):
    """Return a book and calculate fine if any"""
    
    if request.user.role not in ['library', 'admin']:
        return redirect('dashboard')
    
    today = date.today()
    
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        
        try:
            issue = BookIssue.objects.get(id=issue_id, status__in=['issued', 'overdue'])
            
            # Calculate fine
            days_overdue = issue.get_days_overdue()
            fine = days_overdue * 5
            
            # Process return
            issue.return_date = today
            issue.status = 'returned'
            issue.fine_amount = fine
            issue.save()
            
            # Update available copies
            issue.book.available_copies += 1
            issue.book.save()
            
            if fine > 0:
                messages.warning(request, f'Book returned with fine: ৳{fine} (Overdue by {days_overdue} days)')
            else:
                messages.success(request, f'Book "{issue.book.title}" returned successfully')
            
            return redirect('library_dashboard')
            
        except BookIssue.DoesNotExist:
            messages.error(request, 'Invalid issue ID or book already returned')
            return redirect('return_book')
    
    # Show currently issued books for quick reference
    current_issues = BookIssue.objects.filter(status__in=['issued', 'overdue']).select_related('user', 'book')[:20]
    
    # Add due date info to each issue
    for issue in current_issues:
        issue.days_overdue = issue.get_days_overdue()
        issue.days_remaining = issue.get_days_remaining()
        issue.is_overdue = issue.is_overdue()
    
    return render(request, 'library/return_book.html', {
        'current_issues': current_issues,
        'today': today
    })


@login_required
def my_issued_books(request):
    """Students can see their issued books with due date info"""
    
    if request.user.role not in ['medical_student', 'dental_student']:
        return redirect('dashboard')
    
    today = date.today()
    
    issued_books = BookIssue.objects.filter(
        user=request.user,
        status__in=['issued', 'overdue']
    ).select_related('book')
    
    # Calculate due date info for each issue
    for issue in issued_books:
        issue.days_overdue = issue.get_days_overdue()
        issue.days_remaining = issue.get_days_remaining()
        issue.is_overdue = issue.is_overdue()
        if issue.is_overdue:
            issue.fine_amount = issue.days_overdue * 5
    
    history = BookIssue.objects.filter(
        user=request.user,
        status='returned'
    ).select_related('book').order_by('-return_date')[:10]
    
    context = {
        'issued_books': issued_books,
        'history': history,
        'today': today,
    }
    
    return render(request, 'library/my_books.html', context)


@login_required
def reserve_book(request, book_id):
    """Reserve a book if not available"""
    
    book = get_object_or_404(Book, id=book_id)
    
    if request.user.role not in ['medical_student', 'dental_student']:
        messages.error(request, 'Only students can reserve books')
        return redirect('book_detail', book_id=book_id)
    
    # Check if already reserved
    existing_reservation = BookReservation.objects.filter(
        user=request.user,
        book=book,
        status='active'
    ).exists()
    
    if existing_reservation:
        messages.warning(request, 'You already have an active reservation for this book')
    else:
        # Create reservation (expires in 3 days)
        expiry = timezone.now() + timedelta(days=3)
        BookReservation.objects.create(
            user=request.user,
            book=book,
            expiry_date=expiry,
            status='active'
        )
        messages.success(request, f'Book "{book.title}" reserved successfully. Pickup within 3 days.')
    
    return redirect('book_detail', book_id=book_id)


@login_required
def add_book(request):
    """Add new book to library (Library staff only)"""
    
    if request.user.role not in ['library', 'admin']:
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        total_copies = int(request.POST.get('total_copies', 1))
        isbn = request.POST.get('isbn', '')
        publisher = request.POST.get('publisher', '')
        year = request.POST.get('year', '')
        location = request.POST.get('location', '')
        
        book = Book.objects.create(
            title=title,
            author=author,
            category=category,
            total_copies=total_copies,
            available_copies=total_copies,
            isbn=isbn,
            publisher=publisher,
            year=int(year) if year else None,
            location=location
        )
        messages.success(request, f'Book "{book.title}" added successfully')
        return redirect('book_detail', book_id=book.id)
    
    return render(request, 'library/add_book.html')
# ================= WARD POSTING VIEWS =================

@login_required
def ward_posting_schedule(request):
    """Display ward posting schedule"""
    
    today = date.today()
    
    if request.user.role in ['medical_student', 'dental_student', 'intern']:
        # Student view - see their own postings
        postings = WardPosting.objects.filter(
            student=request.user
        ).order_by('-start_date')
        
        active_postings = postings.filter(start_date__lte=today, end_date__gte=today, status='scheduled')
        upcoming_postings = postings.filter(start_date__gt=today, status='scheduled')
        completed_postings = postings.filter(end_date__lt=today, status='completed')
        
    elif request.user.role in ['doctor', 'faculty', 'ward', 'admin']:
        # Staff view - see all postings
        postings = WardPosting.objects.all().order_by('-start_date')
        
        active_postings = postings.filter(start_date__lte=today, end_date__gte=today, status='scheduled')
        upcoming_postings = postings.filter(start_date__gt=today, status='scheduled')
        completed_postings = postings.filter(end_date__lt=today)
        
    else:
        return redirect('dashboard')
    
    # Add additional info to each posting
    for posting in active_postings:
        posting.duration_days = posting.get_duration_days()
        posting.current_shift = posting.get_current_shift()
    
    context = {
        'active_postings': active_postings,
        'upcoming_postings': upcoming_postings,
        'completed_postings': completed_postings,
        'today': today,
        'user_role': request.user.role,
    }
    
    return render(request, 'ward/posting_schedule.html', context)


@login_required
def ward_posting_detail(request, posting_id):
    """View details of a specific ward posting"""
    
    posting = get_object_or_404(WardPosting, id=posting_id)
    
    # Check permission
    if request.user.role not in ['doctor', 'faculty', 'ward', 'admin'] and posting.student != request.user:
        messages.error(request, 'You do not have permission to view this posting')
        return redirect('ward_posting_schedule')
    
    # Get attendance records
    attendances = WardAttendance.objects.filter(posting=posting).order_by('date')
    
    # Calculate statistics
    total_days = posting.get_duration_days()
    present_days = attendances.filter(status='present').count()
    absent_days = attendances.filter(status='absent').count()
    late_days = attendances.filter(status='late').count()
    leave_days = attendances.filter(status='leave').count()
    
    context = {
        'posting': posting,
        'attendances': attendances,
        'total_days': total_days,
        'present_days': present_days,
        'absent_days': absent_days,
        'late_days': late_days,
        'leave_days': leave_days,
        'attendance_percentage': (present_days / total_days * 100) if total_days > 0 else 0,
    }
    
    return render(request, 'ward/posting_detail.html', context)


@login_required
def ward_list(request):
    """Display all wards"""
    
    if request.user.role not in ['doctor', 'faculty', 'ward', 'admin']:
        return redirect('dashboard')
    
    wards = Ward.objects.all().order_by('department', 'name')
    
    # Add statistics for each ward
    for ward in wards:
        ward.active_postings = WardPosting.objects.filter(ward=ward, status='scheduled', end_date__gte=date.today()).count()
        ward.total_students = WardPosting.objects.filter(ward=ward).values('student').distinct().count()
    
    context = {
        'wards': wards,
    }
    
    return render(request, 'ward/ward_list.html', context)


@login_required
def create_ward_posting(request):
    """Create new ward posting (Staff only)"""
    
    if request.user.role not in ['doctor', 'faculty', 'ward', 'admin']:
        messages.error(request, 'You do not have permission to create postings')
        return redirect('dashboard')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        ward_id = request.POST.get('ward_id')
        supervisor_id = request.POST.get('supervisor_id')
        posting_type = request.POST.get('posting_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        remarks = request.POST.get('remarks', '')
        
        try:
            student = User.objects.get(mededu_id=student_id, role__in=['medical_student', 'dental_student', 'intern'])
            ward = Ward.objects.get(id=ward_id)
            supervisor = User.objects.get(id=supervisor_id) if supervisor_id else None
            
            posting = WardPosting.objects.create(
                student=student,
                ward=ward,
                supervisor=supervisor,
                posting_type=posting_type,
                start_date=start_date,
                end_date=end_date,
                remarks=remarks,
                status='scheduled'
            )
            
            messages.success(request, f'Ward posting created successfully for {student.username}')
            return redirect('ward_posting_detail', posting_id=posting.id)
            
        except User.DoesNotExist:
            messages.error(request, 'Student not found')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # Get data for form
    students = User.objects.filter(role__in=['medical_student', 'dental_student', 'intern'], is_verified=True)
    wards = Ward.objects.all()
    supervisors = User.objects.filter(role__in=['doctor', 'faculty'])
    
    context = {
        'students': students,
        'wards': wards,
        'supervisors': supervisors,
    }
    
    return render(request, 'ward/create_posting.html', context)


@login_required
def mark_attendance(request, posting_id):
    """Mark attendance for ward posting"""
    
    posting = get_object_or_404(WardPosting, id=posting_id)
    
    # Check permission
    if request.user.role not in ['doctor', 'faculty', 'ward', 'admin']:
        messages.error(request, 'You do not have permission to mark attendance')
        return redirect('ward_posting_detail', posting_id=posting_id)
    
    if request.method == 'POST':
        date_str = request.POST.get('date')
        status = request.POST.get('status')
        check_in = request.POST.get('check_in_time')
        check_out = request.POST.get('check_out_time')
        remarks = request.POST.get('remarks', '')
        
        try:
            attendance_date = date.fromisoformat(date_str)
            
            attendance, created = WardAttendance.objects.get_or_create(
                posting=posting,
                date=attendance_date,
                defaults={
                    'status': status,
                    'check_in_time': check_in,
                    'check_out_time': check_out,
                    'remarks': remarks,
                    'marked_by': request.user,
                }
            )
            
            if not created:
                # Update existing attendance
                attendance.status = status
                attendance.check_in_time = check_in
                attendance.check_out_time = check_out
                attendance.remarks = remarks
                attendance.marked_by = request.user
                attendance.save()
                messages.success(request, f'Attendance updated for {attendance_date}')
            else:
                messages.success(request, f'Attendance marked for {attendance_date}')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
        
        return redirect('ward_posting_detail', posting_id=posting_id)
    
    context = {
        'posting': posting,
    }
    
    return render(request, 'ward/mark_attendance.html', context)


@login_required
def my_ward_postings(request):
    """Student view - My ward postings"""
    
    if request.user.role not in ['medical_student', 'dental_student', 'intern']:
        return redirect('dashboard')
    
    postings = WardPosting.objects.filter(student=request.user).order_by('-start_date')
    
    context = {
        'postings': postings,
        'today': date.today(),
    }
    
    return render(request, 'ward/my_postings.html', context)


@login_required
def update_posting_status(request, posting_id):
    """Update posting status (Staff only)"""
    
    if request.user.role not in ['doctor', 'faculty', 'ward', 'admin']:
        messages.error(request, 'You do not have permission')
        return redirect('ward_posting_detail', posting_id=posting_id)
    
    posting = get_object_or_404(WardPosting, id=posting_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        posting.status = new_status
        posting.save()
        messages.success(request, f'Posting status updated to {new_status}')
    
    return redirect('ward_posting_detail', posting_id=posting_id)