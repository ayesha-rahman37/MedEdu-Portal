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
    path('pdfs/<int:phase>/', views.phase_pdfs, name='phase_pdfs'),
    path('exam/item/<int:phase>/', views.item_pdf_list, name='item_pdf'),

    # ================= EXAM RESULTS BY PHASE =================
    path('result/<str:exam_type>/<int:phase>/', views.result_by_phase, name='result_phase'),

    # ================= EXAM NOTICES =================
    path('exam/<str:exam_type>/<int:phase>/', views.exam_notice, name='exam_notice'),
    path('admin/add-notice/', views.add_exam_notice, name='add_notice'),

    # ================= DOCTOR SCHEDULE =================
    path("doctor/schedule/", views.doctor_schedule, name="doctor_schedule"),
    
    # ================= LIBRARY URLS =================
    path('library/issue/', views.issue_book, name='issue_book'),
    path('library/return/', views.return_book, name='return_book'),
    path('library/records/', views.records, name='records'),
    path('library/history/', views.history, name='history'),
    path('library/renew/<int:issue_id>/', views.renew_book, name='renew_book'),
    path('library/return-action/<int:issue_id>/', views.return_book_action, name='return_book_action'),
    path('library/my-books/', views.student_library, name='student_library'),

    # ================= INTERN URLS =================
    path('intern/resources/', views.intern_resources, name='intern_resources'),
    
    # ================= PAYMENT URLS =================
    path('payment/', views.payment_dashboard, name='payment'),

    # ================= ELIGIBILITY URLS =================
    path('admin/student-record/', views.student_record_view, name='student_record'),
    path('admin/eligibility/', views.eligibility_view, name='eligibility'),
    path('student/status/', views.student_status_view, name='student_status'),
    
    # ================= FACULTY SCHEDULE =================
    path('faculty/schedule/', views.faculty_schedule, name='faculty_schedule'),
    path("faculty/upload-marks/", views.upload_marks, name="upload_marks"),
    path("faculty/edit-marks/", views.edit_marks, name="edit_marks"),
    path("faculty/attendance/", views.mark_attendance, name="mark_attendance"),
    path('faculty/results/', views.exam_results, name='exam_results'),

    # ================= ANALYTICS URLS =================
    path('analytics/', views.dashboard_analytics, name='analytics'),

    # ================= OT SCHEDULE =================
    path('ot/', views.ot_schedule, name='ot_schedule'),

    # ================= INTERN DUTY SCHEDULE =================
    path('assign-duty/', views.assign_duty, name='assign_duty'),
    path('intern-duty/', views.intern_duty, name='intern_duty'),

    # ================= CLINICAL CASES =================
    path('clinical-case/', views.clinical_case, name='clinical_case'),
]