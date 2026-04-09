from django.urls import path
from . import views

urlpatterns = [

    # ================= HOME =================
    path('', views.home, name="home"),

    # ================= AUTH =================
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),

    # ================= ACCOUNT =================
    path('verify/<int:user_id>/', views.verify_account, name="verify_account"),

    # 🔥 ONLY ONE FORGOT PASSWORD (FIXED)
    path('forgot-password/', views.forgot_password, name='forgot_password'),

    # ================= PROFILE =================
    path('profile/', views.profile_view, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),

    # ================= DASHBOARD =================
    path('dashboard/', views.dashboard_redirect, name="dashboard"),

    # ================= ROLE DASHBOARDS =================
    path('student/dashboard/', views.student_dashboard, name="student_dashboard"),
    path('faculty/dashboard/', views.faculty_dashboard, name="faculty_dashboard"),
    path('intern/dashboard/', views.intern_dashboard, name="intern_dashboard"),
    path('doctor/dashboard/', views.doctor_dashboard, name="doctor_dashboard"),
    path('ward/dashboard/', views.ward_dashboard, name="ward_dashboard"),
    path('library/dashboard/', views.library_dashboard, name="library_dashboard"),
    path('admin/dashboard/', views.admin_dashboard, name="admin_dashboard"),

    # ================= SUBJECTS & EXAMS =================
    path("subjects/", views.subject_list, name="subjects"),
    # path("subject/<str:name>/", views.subject_detail, name="subject_detail"),
    path("subject/<slug:slug>/", views.subject_detail, name="subject_detail"),
    path("exam/", views.exam_page, name="exam"),
    path("result/", views.result_page, name="result"),
]