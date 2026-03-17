from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import User


# HOME PAGE
def home(request):
    return render(request, "home.html")


# SIGNUP
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        role = request.POST.get("role")
        password = request.POST.get("password")

        user = User.objects.create(
            username=username,
            email=email,
            phone=phone,
            role=role
        )

        user.set_password(password)

        # Unique MedEdu ID generate

        if role == "student":
            prefix = "S"

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

        return render(request, "signup_success.html", {"mededu_id": user.mededu_id})

    return render(request, "signup.html")


# LOGIN
def login_view(request):

    if request.method == "POST":

        mededu_id = request.POST.get("mededu_id")
        password = request.POST.get("password")

        try:
            user = User.objects.get(mededu_id=mededu_id)

            if user.check_password(password):

                login(request, user)

                # IMPORTANT: redirect to dashboard (NOT admin)
                return redirect("dashboard")

        except User.DoesNotExist:
            return render(request,"login.html",{"error":"Invalid ID or password"})

    return render(request,"login.html")


# LOGOUT
def logout_view(request):

    logout(request)

    return redirect("home")


# PROFILE
@login_required
def profile_view(request):

    return render(request, "profile.html")


# DASHBOARD REDIRECT
@login_required
def dashboard_redirect(request):

    role = request.user.role

    if role == "admin":
        return redirect("admin_dashboard")

    elif role == "student":
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

    return redirect("home")


# DASHBOARDS

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