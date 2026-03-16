from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import SignupForm
from .models import User


def home(request):
    return render(request, "home.html")


# SIGNUP
def signup_view(request):

    form = SignupForm(request.POST or None)

    if form.is_valid():

        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        return render(request, "signup_success.html", {
            "mededu_id": user.mededu_id
        })

    return render(request, "signup.html", {"form": form})


# LOGIN
def login_view(request):

    if request.method == "POST":

        mededu_id = request.POST.get("mededu_id")
        password = request.POST.get("password")

        try:
            user = User.objects.get(mededu_id=mededu_id)

            if user.check_password(password):

                login(request, user)
                return redirect("profile")

        except User.DoesNotExist:
            return render(request, "login.html", {
                "error": "Invalid MedEdu ID or Password"
            })

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile_view(request):
    return render(request, "profile.html")