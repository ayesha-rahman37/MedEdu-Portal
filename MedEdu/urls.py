from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.home, name="home"),

    # Authentication
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # Profile
    path('profile/', views.profile_view, name="profile"),

    # Dashboard redirect (role detect করবে)
    path('dashboard/', views.dashboard_redirect, name="dashboard"),

    # Role based dashboards
    path('student/dashboard/', views.student_dashboard, name="student_dashboard"),

    path('faculty/dashboard/', views.faculty_dashboard, name="faculty_dashboard"),

    path('intern/dashboard/', views.intern_dashboard, name="intern_dashboard"),

    path('doctor/dashboard/', views.doctor_dashboard, name="doctor_dashboard"),

    path('ward/dashboard/', views.ward_dashboard, name="ward_dashboard"),

    path('library/dashboard/', views.library_dashboard, name="library_dashboard"),

    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),

]