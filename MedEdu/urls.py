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

    # ONLY ONE FORGOT PASSWORD (FIXED)
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
    path("subject/<slug:slug>/", views.subject_detail, name="subject_detail"),
    path("exam/", views.exam_page, name="exam"),
    path("result/", views.result_page, name="result"),

    # ================= DOCTOR SCHEDULE =================
    path("doctor/schedule/", views.doctor_schedule, name="doctor_schedule"),
    
    # ================= LIBRARY URLS =================
    path('library/books/', views.book_list, name="book_list"),
    path('library/book/<int:book_id>/', views.book_detail, name="book_detail"),
    path('library/issue/', views.issue_book, name="issue_book"),
    path('library/return/', views.return_book, name="return_book"),
    path('library/my-books/', views.my_issued_books, name="my_issued_books"),
    path('library/reserve/<int:book_id>/', views.reserve_book, name="reserve_book"),
    path('library/add-book/', views.add_book, name="add_book"),
    
        # ================= WARD POSTING URLS =================
    path('ward/schedule/', views.ward_posting_schedule, name="ward_posting_schedule"),
    path('ward/posting/<int:posting_id>/', views.ward_posting_detail, name="ward_posting_detail"),
    path('ward/list/', views.ward_list, name="ward_list"),
    path('ward/create/', views.create_ward_posting, name="create_ward_posting"),
    path('ward/attendance/<int:posting_id>/', views.mark_attendance, name="mark_attendance"),
    path('ward/my-postings/', views.my_ward_postings, name="my_ward_postings"),
    path('ward/update-status/<int:posting_id>/', views.update_posting_status, name="update_posting_status"),
]