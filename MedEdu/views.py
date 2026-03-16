from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import SignupForm
from .models import User


def home(request):

    return render(request, "home.html")


def signup_view(request):

    form = SignupForm(request.POST or None)

    mededu_id = None

    if form.is_valid():

        user = form.save(commit=False)

        user.set_password(form.cleaned_data['password'])

        user.save()

        mededu_id = user.meded_id

    return render(request, "signup.html", {
        "form": form,
        "mededu_id": mededu_id
    })


def login_view(request):

    if request.method == "POST":

        mededu_id = request.POST.get("mededu_id")

        password = request.POST.get("password")

        try:

            user = User.objects.get(mededu_id=mededu_id)

            if user.check_password(password):

                login(request, user)

                return redirect("dashboard")

        except User.DoesNotExist:

            pass

    return render(request, "login.html")


def logout_view(request):

    logout(request)

    return redirect("home")


@login_required
def dashboard_redirect(request):

    role = request.user.role

    if role == "student":
        return redirect("student_dashboard")

    elif role == "doctor":
        return redirect("doctor_dashboard")

    elif role == "faculty":
        return redirect("faculty_dashboard")

    elif role == "intern":
        return redirect("intern_dashboard")

    elif role == "library":
        return redirect("library_dashboard")

    elif role == "ward":
        return redirect("ward_dashboard")

    elif role == "admin":
        return redirect("admin_dashboard")

    return redirect("home")


@login_required
def student_dashboard(request):
    return render(request, "dashboards/student_dashboard.html")


@login_required
def doctor_dashboard(request):
    return render(request, "dashboards/doctor_dashboard.html")


@login_required
def faculty_dashboard(request):
    return render(request, "dashboards/faculty_dashboard.html")


@login_required
def intern_dashboard(request):
    return render(request, "dashboards/intern_dashboard.html")


@login_required
def library_dashboard(request):
    return render(request, "dashboards/library_dashboard.html")


@login_required
def ward_dashboard(request):
    return render(request, "dashboards/ward_dashboard.html")


@login_required
def admin_dashboard(request):
    return render(request, "dashboards/admin_dashboard.html")


@login_required
def profile_view(request):

    return render(request, "profile.html")