from pydoc_data.topics import topics
from urllib import request

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import User, Subject, Topic, ExamSchedule, Result
from django.shortcuts import render, get_object_or_404

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
    subject = get_object_or_404(Subject, slug=slug)
    topics = Topic.objects.filter(subject=subject)

    user = request.user

    # 🔥 course detect (IMPORTANT - uppercase folder match)
    if user.role == "medical_student":
        course = "MBBS"
    elif user.role == "dental_student":
        course = "BDS"

    # 🔥 EXACT PDF PATH (your real files)
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
        ]

        # # ===== EXTRA FILE =====
        # "internship": f"/static/pdfs/{course}/Internship.pdf",
        # "extras": [
        #     f"/static/pdfs/{course}/Phase 1/Anatomy Card.pdf",
        #     f"/static/pdfs/{course}/Internship.pdf",
        # ]
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

    return render(request, "subject_detail.html", {
        "subject": subject,
        "topics": topics,
        "pdf_path": pdf_path,
        "extra_pdfs": extra_pdfs
    })



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