from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from .models import User


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

        # 🔥 duplicate check
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

        # ===== MedEdu ID generate =====
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

        # ===== EMAIL VERIFICATION =====
        link = request.build_absolute_uri(
            reverse("verify_account", args=[user.id])
        )

        send_mail(
            "Verify Your Account",
            f"Click this link to verify your account: {link}",
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

            # 🔥 CHECK PASSWORD
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


# ================= FORGOT PASSWORD =================
def forgot_password(request):

    if request.method == "POST":

        mededu_id = request.POST.get("mededu_id")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # 🔥 check empty
        if not mededu_id or not new_password or not confirm_password:
            return render(request, "reset.html", {
                "error": "All fields are required"
            })

        # 🔥 check password match
        if new_password != confirm_password:
            return render(request, "reset.html", {
                "error": "Passwords do not match"
            })

        try:
            user = User.objects.get(mededu_id=mededu_id)

            user.set_password(new_password)
            user.save()

            return render(request, "reset.html", {
                "success": "Password reset successful! Now login."
            })

        except User.DoesNotExist:
            return render(request, "reset.html", {
                "error": "Invalid MedEdu ID"
            })

    return render(request, "reset.html")


# ================= PROFILE =================
@login_required
def profile_view(request):
    return render(request, "profile.html")


# ================= PROFILE EDIT =================
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
    return render(request, "dashboards/student_dashboard.html")


@login_required
def faculty_dashboard(request):
    return render(request, "dashboards/faculty_dashboard.html")


@login_required
def intern_dashboard(request):
    return render(request, "dashboards/intern_dashboard.html")


@login_required
def doctor_dashboard(request):
    return render(request, "dashboards/doctor_dashboard.html")


@login_required
def ward_dashboard(request):
    return render(request, "dashboards/ward_dashboard.html")


@login_required
def library_dashboard(request):
    return render(request, "dashboards/library_dashboard.html")


@login_required
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")