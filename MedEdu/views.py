from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import DutySchedule, ClinicalCase, DutySwapRequest, User, Subject, Topic, ExamSchedule, Result, DoctorSchedule, Book, Issue, ExamNotice, Payment, Salary, StudentRecord, WardSwapRequest, ClassSchedule,  Attendance, Notification, OperationSchedule, WardPosting
from django.shortcuts import render, get_object_or_404
from datetime import date, timedelta

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

    return render(request, "dashboards/student_dashboard.html", {
        "role": role
    })


@login_required
def faculty_dashboard(request):
    role = request.user.role.replace("_", " ").title()

    return render(request, "dashboards/faculty_dashboard.html", {
        "role": role
    })


@login_required
def intern_dashboard(request):
    role = request.user.role.replace("_", " ").title()

    return render(request, "dashboards/intern_dashboard.html", {
        "role": role
    })


@login_required
def doctor_dashboard(request):
    role = request.user.role.replace("_", " ").title()

    return render(request, "dashboards/doctor_dashboard.html", {
        "role": role
    })


@login_required
def ward_dashboard(request):
    role = request.user.role.replace("_", " ").title()

    return render(request, "dashboards/ward_dashboard.html", {
        "role": role
    })


@login_required
def library_dashboard(request):
    role = request.user.role.replace("_", " ").title()

    return render(request, "dashboards/library_dashboard.html", {
        "role": role
    })


@login_required
def admin_dashboard(request):
    role = request.user.role.replace("_", " ").title()

    return render(request, "dashboards/admin_dashboard.html", {
        "role": role
    })


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

    # only students allowed
    if request.user.role not in ["medical_student", "dental_student"]:
        return redirect("dashboard")

    subject = get_object_or_404(Subject, slug=slug)
    topics = Topic.objects.filter(subject=subject)

    user = request.user

    # course detect
    if user.role == "medical_student":
        course = "MBBS"
    elif user.role == "dental_student":
        course = "BDS"
    else:
        course = "MBBS"

    # PDF map (unchanged)
    pdf_map = {

        # MBBS (phase 1)
        "anatomy": f"/static/pdfs/{course}/Phase 1/Anatomy.pdf",
        "physiology": f"/static/pdfs/{course}/Phase 1/Physiology.pdf",
        "biochemistry": f"/static/pdfs/{course}/Phase 1/Biochemistry.pdf",

        # MBBS (phase 2)
        "pharmacology-therapeutics": f"/static/pdfs/{course}/Phase 2/Pharmacology & Therapeutics.pdf",
        "forensic-medicine-toxicology": f"/static/pdfs/{course}/Phase 2/Forensic Medicine & Toxicology.pdf",

        # MBBS (phase 3)
        "general-pathology-basic": f"/static/pdfs/{course}/Phase 3/Pathology.pdf",
        "general-microbiology-basic": f"/static/pdfs/{course}/Phase 3/Microbiology.pdf",
        "community-medicine-public-health": f"/static/pdfs/{course}/Phase 3/Community Medicine & Public Health.pdf",

        # MBBS (phase 4)
        "medicine-intro": f"/static/pdfs/{course}/Phase 4/Medicine.pdf",
        "surgery-intro": f"/static/pdfs/{course}/Phase 4/Surgery & Allied Subjects.pdf",
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

        # BDS (phase 1)
        "general-anatomy": f"/static/pdfs/{course}/Phase 1/Anatomy (Paper - I).pdf",
        "dental-anatomy": f"/static/pdfs/{course}/Phase 1/Dental Anatomy (Paper - II).pdf",
        "physiology-biochemistry": f"/static/pdfs/{course}/Phase 1/Physiology & Biochemistry.pdf",
        "science-of-dental-materials": f"/static/pdfs/{course}/Phase 1/Science of Dental Materials.pdf",

        # BDS (phase 2)
        "general-pharmacology-dental-therapeutics": f"/static/pdfs/{course}/Phase 2/General Pharmacology & Dental Therapeutics.pdf",
        "pathology-microbiology": f"/static/pdfs/{course}/Phase 2/Pathology & Microbiology.pdf",

        # BDS (phase 3)
        "medicine-bds": f"/static/pdfs/{course}/Phase 3/Medicine.pdf",
        "surgery-bds": f"/static/pdfs/{course}/Phase 3/Surgery.pdf",
        "periodontology-oral-pathology": f"/static/pdfs/{course}/Phase 3/Periodontology & Oral Pathology.pdf",

        # BDS (phase 4)
        "oral-maxillofacial-surgery": f"/static/pdfs/{course}/Phase 4/Oral & Maxillofacial Surgery.pdf",
        "conservative-dentistry-endodontics": f"/static/pdfs/{course}/Phase 4/Conservative Dentistry & Endodontics.pdf",
        "prosthodontics": f"/static/pdfs/{course}/Phase 4/Prosthodontics.pdf",
        "orthodontics-dentofacial-orthopedics": f"/static/pdfs/{course}/Phase 4/Orthodontics & Dentofacial Orthopedics.pdf",
        "pedodontics-dental-public-health": f"/static/pdfs/{course}/Phase 4/Pedodontics & Dental Public Health.pdf",
    }

    # main pdf
    data = pdf_map.get(slug)
    pdf_path = data if isinstance(data, str) else None

    # extra pdf (phase 4 subjects)
    extra_pdfs = []
    if slug in ["medicine", "surgery", "obstetrics-gynaecology"]:
        extra_pdfs = pdf_map.get("extras", [])

    # =========================
    # 🔥 FIXED ADDITIONAL RESOURCES
    # =========================

    additional_resources = []

    # only current phase IT
    additional_resources.append({
        "name": f"IT (Phase {subject.phase})",
        "file": f"/static/pdfs/{course}/Phase {subject.phase}/IT Phase {subject.phase}.pdf"
    })

    # internship only phase 4
    if subject.phase == 4:
        additional_resources.append({
            "name": "Internship",
            "file": f"/static/pdfs/{course}/Internship.pdf"
        })

    # prescription only intern role
    if hasattr(request.user, "role") and request.user.role == "intern":
        additional_resources.append({
            "name": "Prescription",
            "file": f"/static/pdfs/{course}/Prescription.pdf"
        })

    return render(request, "subject_detail.html", {
        "subject": subject,
        "topics": topics,
        "pdf_path": pdf_path,
        "extra_pdfs": extra_pdfs,
        "additional_resources": additional_resources
    })


# ================= EXAM PAGE =================
@login_required
def exam_page(request):

    # 🔥 optional: filter based on student type
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

    # 🔥 ONLY own result
    results = Result.objects.filter(user=request.user)

    return render(request, "result.html", {
        "results": results
    })

# ================= DOCTOR SCHEDULE =================

@login_required
def doctor_schedule(request):

    # DEBUG (optional)
    print(DoctorSchedule.objects.all())

    # ❌ doctor না হলে block
    if request.user.role != "doctor":
        return render(request, "access_denied.html")

    # ✅ today's date
    today = date.today()

    # ✅ today's schedules
    today_schedules = DoctorSchedule.objects.filter(
        doctor=request.user,
        date=today
    ).order_by("start_time")

    # ✅ all schedules
    schedules = DoctorSchedule.objects.filter(
        doctor=request.user
    ).order_by("date", "start_time")

    # ✅ FINAL RETURN (IMPORTANT)
    return render(request, "doctor_schedule.html", {
        "today_schedules": today_schedules,
        "schedules": schedules
    })


# ================= LIBRARY =================

@login_required
def library_dashboard(request):

    books = Book.objects.count()
    available = Book.objects.filter(available_copies__gt=0).count()
    issued = Issue.objects.filter(returned=False).count()
    overdue = Issue.objects.filter(returned=False, due_date__lt=date.today()).count()

    recent = Issue.objects.order_by('-issue_date')[:5]

    return render(request, 'dashboards/library_dashboard.html', {
        'books': books,
        'available': available,
        'issued': issued,
        'overdue': overdue,
        'recent': recent
    })


# ================= ISSUE BOOK =================
@login_required
def issue_book(request):

    users = User.objects.all()
    books = Book.objects.all()

    if request.method == 'POST':

        student_id = request.POST.get('student')
        book_id = request.POST.get('book')
        due_date = request.POST.get('due_date')

        student = User.objects.get(id=student_id)
        book = Book.objects.get(id=book_id)

        if book.available_copies > 0:
            Issue.objects.create(
                student=student,
                book=book,
                due_date=due_date
            )

            book.available_copies -= 1
            book.save()

        return redirect('library_dashboard')

    return render(request, 'library/issue_book.html', {
        'users': users,
        'books': books
    })


# ================= RETURN PAGE =================
@login_required
def return_book(request):

    issued_books = Issue.objects.filter(returned=False)

    return render(request, 'library/return_book.html', {
        'issued_books': issued_books
    })


# ================= RETURN ACTION =================
@login_required
def return_book_action(request, issue_id):

    issue = Issue.objects.get(id=issue_id)

    if not issue.returned:
        issue.returned = True
        issue.save()

        book = issue.book
        book.available_copies += 1
        book.save()

    return redirect('return_book')


# ================= RECORDS =================
@login_required
def records(request):

    books = Book.objects.all()

    return render(request, 'library/records.html', {
        'books': books
    })


# ================= HISTORY =================
@login_required
def history(request):

    history = Issue.objects.all().order_by('-issue_date')

    return render(request, 'library/history.html', {
        'history': history
    })
    
# ================= FINE CALCULATION =================
@login_required
def calculate_fine(issue):
    if issue.returned:
        return 0

    today = date.today()
    if today > issue.due_date:
        days = (today - issue.due_date).days
        return days * 2   # 2 taka per day
    return 0

# ================= RENEW BOOK =================
def renew_book(request, issue_id):
    issue = Issue.objects.get(id=issue_id)

    issue.due_date = issue.due_date + timedelta(days=7)
    issue.save()

    return redirect('my_books')

# ================= STUDENT LIBRARY VIEW =================
@login_required
def student_library(request):
    user = request.user

    issues = Issue.objects.filter(student=user)

    return render(request, 'library/my_books.html', {
        'issues': issues
    })

# ================= PDF LISTING =================
@login_required
def phase_pdfs(request, phase):
    import os

    base_path = f"static/pdf/MBBS/phase{phase}"
    files = []

    if os.path.exists(base_path):
        for f in os.listdir(base_path):
            if f.endswith(".pdf"):
                files.append(f)

    return render(request, 'pdf_list.html', {
        'files': files,
        'phase': phase
    })

# ================= RESULT BY PHASE =================
@login_required
def result_by_phase(request, exam_type, phase):

    # logged in user
    user = request.user

    # filter topics by phase
    topics = Topic.objects.filter(subject__phase=phase)

    # filter results
    results = Result.objects.filter(
        user=user,
        topic__in=topics
    )

    context = {
        'results': results,
        'exam_type': exam_type,
        'phase': phase,
    }

    return render(request, 'result/result_list.html', context)


#================= INTERN RESOURCES =================
@login_required
def intern_resources(request):

    if request.user.role != "intern":
        return redirect("dashboard")

    resources = [
        {
            "name": "Internship",
            "file": "/static/pdfs/MBBS/Internship.pdf"
        },
        {
            "name": "Prescription",
            "file": "/static/pdfs/MBBS/Prescription.pdf"
        }
    ]

    return render(request, "intern_resources.html", {
        "resources": resources
    })


@login_required
def item_pdf_list(request, phase):

    user = request.user

    # Safety guard (prevents crash)
    if not hasattr(user, "role"):
        return redirect('login')

    # course detect
    if user.role == "medical_student":
        course = "MBBS"
    elif user.role == "dental_student":
        course = "BDS"
    else:
        course = "MBBS"

    # MANUAL CONTROL (UNCHANGED)
    pdf_data = {

        "MBBS": {
            1: ["Anatomy Card.pdf", "Biochemistry Card.pdf", "Physiology Card.pdf"],
            2: ["Forensic Medicine & Toxicology Card.pdf", "Pharmacology & Therapeutics Card.pdf"],
            3: ["Microbiology.pdf", "Pathology.pdf"],
            4: ["Opthalmology Card.pdf", "Otorhinolaryngology & Head-Neck Surgery Card.pdf", "Psychiatry Card.pdf", "Skin & VD Card.pdf", "Surgery Card.pdf"],
        },

        "BDS": {
            1: ["Anatomy Card.pdf", "Physiology & Biochemistry Card.pdf", "Science of Dental Materials Card.pdf"],
            2: ["General Pharmacology & Dental Therapeutics Card.pdf", "Pathology & Microbiology Card.pdf"],
            3: [
                "Medicine Card.pdf",
                "Periodontology & Oral Pathology Card.pdf"
            ],
            4: ["Conservative Dentistry & Endodontics Card.pdf", "Pedodontics & Dental Public Health Card.pdf", "Pedodontics Card.pdf"],
        }

    }

    files = pdf_data.get(course, {}).get(int(phase), [])

    context = {
        'files': files,
        'phase': phase,
        'course': course,
    }

    return render(request, 'pdf_list.html', context)

# ================= EXAM NOTICE =================
@login_required
def exam_notice(request, exam_type, phase):

    user = request.user

    if user.role == "medical_student":
        course = "MBBS"
    else:
        course = "BDS"

    notices = ExamNotice.objects.filter(
        exam_type=exam_type,
        phase=phase,
        course=course
    )

    return render(request, 'exam_notice.html', {'notices': notices})

# ================= ADD EXAM NOTICE (ADMIN) =================
@login_required
def add_exam_notice(request):

    if request.user.role != "admin":
        return redirect('home')

    if request.method == "POST":
        exam_type = request.POST.get('exam_type')
        course = request.POST.get('course')
        phase = request.POST.get('phase')
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')

        ExamNotice.objects.create(
            exam_type=exam_type,
            course=course,
            phase=phase,
            title=title,
            description=description,
            date=date
        )

        return redirect('add_notice')

    return render(request, 'add_notice.html')


# ================= PAYMENT DASHBOARD =================
@login_required
def payment_dashboard(request):

    user = request.user

    # STUDENT
    if user.role in ["medical_student", "dental_student"]:

        if request.method == "POST":
            amount = request.POST.get("amount")
            method = request.POST.get("method")
            purpose = request.POST.get("purpose")
            bank = request.POST.get("bank")

            if amount and method and purpose:
                Payment.objects.create(
                    user=user,
                    amount=int(amount),
                    method=method,
                    purpose=purpose,
                    bank_name=bank
                )

        payments = Payment.objects.filter(user=user).order_by('-date')
        total_paid = sum(p.amount for p in payments)

        return render(request, "payment/student_payment.html", {
            "payments": payments,
            "total_paid": total_paid,
        })

    # DOCTOR / INTERN
    elif user.role in ["doctor", "intern"]:

        salaries = Salary.objects.filter(user=user)

        return render(request, "payment/salary.html", {
            "salaries": salaries
        })

# ================ STUDENT ELIGIBILITY CHECK =================
def check_eligibility(record):

    if record.attendance < 75:
        return "Not Eligible (Low Attendance)"

    if not record.item_pass:
        return "Not Eligible for Card"

    if record.item_pass and not record.card_pass:
        return "Eligible for Card"

    if record.card_pass and not record.term_pass:
        return "Eligible for Term"

    if record.term_pass:
        return "Eligible for Professional Exam"

    return "Not Eligible"

# ================= STUDENT RECORD VIEW (ADMIN) =================
@login_required
def student_record_view(request):

    if request.user.role != "admin":
        return redirect("dashboard")

    records = StudentRecord.objects.select_related("user")

    return render(request, "admin/student_record.html", {
        "records": records
    })


@login_required
def eligibility_view(request):

    if request.user.role != "admin":
        return redirect("dashboard")

    records = StudentRecord.objects.all()

    data = []
    for r in records:
        status = check_eligibility(r)
        data.append({
            "user": r.user,
            "status": status
        })

    return render(request, "admin/eligibility.html", {
        "data": data
    })

# ================= STUDENT STATUS VIEW (STUDENT) =================
@login_required
def student_status_view(request):

    record = StudentRecord.objects.filter(user=request.user).first()

    if not record:
        return render(request, "student/status.html", {"status": "No Data"})

    status = check_eligibility(record)

    return render(request, "student/status.html", {
        "status": status
    })


# ================= FACULTY SCHEDULE =================
@login_required
def faculty_schedule(request):

    if request.user.role != "faculty":
        return redirect("dashboard")

    schedules = ClassSchedule.objects.filter(faculty=request.user).order_by("date", "start_time")

    return render(request, "faculty/schedule.html", {
        "schedules": schedules
    })
    

# ================= UPLOAD MARKS =================
@login_required
def upload_marks(request):

    if request.user.role != "faculty":
        return redirect("dashboard")

    students = User.objects.filter(role__in=["medical_student", "dental_student"])
    topics = Topic.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student")
        topic_id = request.POST.get("topic")
        marks = int(request.POST.get("marks"))

        student = User.objects.get(id=student_id)
        topic = Topic.objects.get(id=topic_id)

        # PASS/FAIL LOGIC (60%)
        if marks >= (topic.full_marks * 0.6):
            status = "clear"
        else:
            status = "pending"

        Result.objects.update_or_create(
            user=student,
            topic=topic,
            defaults={
                "marks": marks,
                "status": status,
                "date": date.today()
            }
        )

        return redirect("upload_marks")

    return render(request, "faculty/upload_marks.html", {
        "students": students,
        "topics": topics
    })
    

# ================= EDIT MARKS =================
@login_required
def edit_marks(request):

    if request.user.role != "faculty":
        return redirect("dashboard")

    results = Result.objects.select_related("user", "topic").all()

    if request.method == "POST":
        result_id = request.POST.get("result_id")
        new_marks = int(request.POST.get("marks"))

        result = Result.objects.get(id=result_id)

        # pass/fail update
        if new_marks >= (result.topic.full_marks * 0.6):
            result.status = "clear"
        else:
            result.status = "pending"

        result.marks = new_marks
        result.save()

        return redirect("edit_marks")

    return render(request, "faculty/edit_marks.html", {
        "results": results
    })
    
    

# ================= MARK ATTENDANCE =================
@login_required
def mark_attendance(request):

    if request.user.role != "faculty":
        return redirect("dashboard")

    students = User.objects.filter(role__in=["medical_student", "dental_student"])
    subjects = Subject.objects.all()

    if request.method == "POST":
        student_id = request.POST.get("student")
        subject_id = request.POST.get("subject")
        status = request.POST.get("status")

        student = User.objects.get(id=student_id)
        subject = Subject.objects.get(id=subject_id)

        Attendance.objects.create(
            student=student,
            subject=subject,
            date=date.today(),
            status=status
        )

        return redirect("mark_attendance")

    return render(request, "faculty/attendance.html", {
        "students": students,
        "subjects": subjects
    })
    
    
# ================= EXAM RESULTS VIEW (FACULTY) =================
@login_required
def exam_results(request):

    # only faculty allowed
    if request.user.role != "faculty":
        return redirect("dashboard")

    results = Result.objects.select_related('user', 'topic')

    data = []

    for r in results:
        if r.marks is not None:
            percent = (r.marks / r.topic.full_marks) * 100
            status = "Pass" if percent >= 60 else "Fail"
        else:
            percent = 0
            status = "Pending"

        data.append({
            "student": r.user.username,
            "topic": r.topic.title,
            "marks": r.marks,
            "percent": round(percent, 2),
            "status": status
        })

    return render(request, "faculty/exam_results.html", {
        "data": data
    })


# ================= DASHBOARD ANALYTICS =================
@login_required
def dashboard_analytics(request):

    if request.user.role == "faculty" or request.user.role == "admin":
        results = Result.objects.all()
    else:
        results = Result.objects.filter(user=request.user)

    total = results.count()

    if total == 0:
        return render(request, "analytics.html", {"no_data": True})

    marks_list = []
    pass_count = 0

    for r in results:
        if r.marks is not None:
            percent = (r.marks / r.topic.full_marks) * 100
            marks_list.append(percent)

            if percent >= 60:
                pass_count += 1

    avg = sum(marks_list) / len(marks_list) if marks_list else 0
    pass_rate = (pass_count / total) * 100

    # 🔥 Improvement Logic (last 5 vs previous 5)
    last5 = marks_list[-5:]
    prev5 = marks_list[:-5]

    if prev5:
        prev_avg = sum(prev5) / len(prev5)
        improvement = avg - prev_avg
    else:
        improvement = 0

    return render(request, "analytics.html", {
        "avg": round(avg, 2),
        "pass_rate": round(pass_rate, 2),
        "total": total,
        "improvement": round(improvement, 2)
    })


# ================= OT SCHEDULE VIEW =================
@login_required
def ot_schedule(request):
    user = request.user

    # doctor view
    if user.role == "doctor":
        schedules = OperationSchedule.objects.filter(doctor=user)

    # student + intern view
    elif user.role in ["medical_student", "dental_student", "intern"]:
        schedules = OperationSchedule.objects.filter(participants=user)

    else:
        schedules = []

    return render(request, "ot/schedule.html", {
        "schedules": schedules
    })




# ================= ADMIN ASSIGN DUTY =================
@login_required
def assign_duty(request):
    if request.user.role != "admin":
        return redirect("dashboard")

    users = User.objects.filter(role__in=["intern", "student"])

    if request.method == "POST":
        user_id = request.POST.get("user")
        role_type = request.POST.get("role_type")
        ward = request.POST.get("ward")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        task = request.POST.get("task")
        doctor_id = request.POST.get("doctor")
        round_required = request.POST.get("round") == "on"

        user = User.objects.get(id=user_id)
        doctor = User.objects.get(id=doctor_id) if doctor_id else None

        DutySchedule.objects.create(
            user=user,
            role_type=role_type,
            ward=ward,
            date=date,
            start_time=start_time,
            end_time=end_time,
            task=task,
            doctor=doctor,
            round_required=round_required
        )

        return redirect("assign_duty")

    doctors = User.objects.filter(role="doctor")

    return render(request, "admin/assign_duty.html", {
        "users": users,
        "doctors": doctors
    })


# ================= INTERN/STUDENT VIEW =================
@login_required
def intern_duty(request):
    duties = DutySchedule.objects.filter(user=request.user).order_by('-date')

    return render(request, "intern/duty.html", {
        "duties": duties
    })


# ================= REQUEST DUTY SWAP =================
@login_required
def request_swap(request, duty_id):
    duty = DutySchedule.objects.get(id=duty_id)

    if request.method == "POST":
        to_user_id = request.POST.get("to_user")

        to_user = User.objects.get(id=to_user_id)

        DutySwapRequest.objects.create(
            from_user=request.user,
            to_user=to_user,
            duty=duty
        )

    return redirect("intern_duty")


@login_required
def clinical_case(request):
    if request.user.role != "intern":
        return redirect("dashboard")

    if request.method == "POST":
        patient_name = request.POST.get("patient_name")
        phone = request.POST.get("phone")
        disease = request.POST.get("disease")
        history = request.POST.get("history")

        ClinicalCase.objects.create(
            intern=request.user,
            patient_name=patient_name,
            phone=phone,
            disease=disease,
            history=history
        )

        return redirect("clinical_case")

    cases = ClinicalCase.objects.filter(intern=request.user).order_by("-created_at")

    return render(request, "intern/clinical_case.html", {
        "cases": cases
    })

# ================= NOTIFICATIONS VIEW =================
@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    # mark as read when opened
    notifications.update(is_read=True)

    return render(request, 'notifications.html', {
        'notifications': notifications
    })
    
    
    
# ================= WARD POSTING =================
@login_required
def ward_posting_manage(request):

    if request.user.role != "ward":
        return redirect("home")

    users = User.objects.filter(
        role__in=["medical_student", "dental_student", "intern"]
    )

    if request.method == "POST":

        user_id = request.POST.get("user")
        ward_name = request.POST.get("ward_name")
        duty_type = request.POST.get("duty_type")
        date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        selected_user = User.objects.get(id=user_id)

        role_type = "student"

        if selected_user.role == "intern":
            role_type = "intern"

        WardPosting.objects.create(
            user=selected_user,
            role_type=role_type,
            ward_name=ward_name,
            duty_type=duty_type,
            date=date,
            start_time=start_time,
            end_time=end_time,
            assigned_by=request.user
        )

        return redirect("ward_posting_manage")

    postings = WardPosting.objects.all().order_by("-date")

    return render(request, "ward/manage_posting.html", {
        "users": users,
        "postings": postings
    })
    
@login_required
def my_ward_posting(request):

    postings = WardPosting.objects.filter(
        user=request.user
    ).order_by("-date")

    return render(request, "ward/my_posting.html", {
        "postings": postings
    })
    
@login_required
def ward_swap_request(request, posting_id):

    posting = WardPosting.objects.get(id=posting_id)

    users = User.objects.filter(
        role=posting.user.role
    ).exclude(id=request.user.id)

    if request.method == "POST":

        swap_user = request.POST.get("swap_with")
        reason = request.POST.get("reason")

        WardSwapRequest.objects.create(
            posting=posting,
            requested_by=request.user,
            swap_with_id=swap_user,
            reason=reason
        )

        return redirect("my_ward_posting")

    return render(request, "ward/swap_request.html", {
        "posting": posting,
        "users": users
    })
    
@login_required
def ward_swap_requests(request):

    if request.user.role != "ward":
        return redirect("home")

    requests = WardSwapRequest.objects.all().order_by("-created_at")

    return render(request, "ward/swap_requests.html", {
        "requests": requests
    })


@login_required
def update_swap_status(request, request_id, action):

    swap = WardSwapRequest.objects.get(id=request_id)

    if action == "accept":
        swap.status = "accepted"

    elif action == "reject":
        swap.status = "rejected"

    swap.save()

    return redirect("ward_swap_requests")
    
