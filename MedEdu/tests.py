from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import (
    ExamNotice, Book, Issue, Subject,
    Payment, StudentRecord, Salary
)

User = get_user_model()


class MedEduTest(TestCase):

    def setUp(self):
        # ================= USERS =================
        self.student = User.objects.create(
            username='student1',
            role='medical_student',
            is_verified=True
        )
        self.student.set_password('12345')
        self.student.mededu_id = "MS-1001"
        self.student.save()

        self.admin = User.objects.create(
            username='admin1',
            role='admin',
            is_verified=True
        )
        self.admin.set_password('12345')
        self.admin.mededu_id = "A-1009"
        self.admin.save()

        self.doctor = User.objects.create(
            username='doctor1',
            role='doctor',
            is_verified=True
        )
        self.doctor.set_password('12345')
        self.doctor.save()

        # ================= SUBJECT =================
        self.subject = Subject.objects.create(
            name="Anatomy",
            slug="anatomy",
            phase=1,
            course_type="MBBS"
        )

    # ================= AUTH =================

    def test_login_success(self):
        response = self.client.post(reverse("login"), {
            "mededu_id": "MS-1001",
            "password": "12345"
        })
        self.assertEqual(response.status_code, 302)

    def test_login_fail(self):
        response = self.client.post(reverse("login"), {
            "mededu_id": "MS-1001",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 200)

    # ================= DASHBOARD =================

    def test_dashboard_redirect(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)

    def test_student_dashboard_access(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/student/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get('/student/dashboard/')
        self.assertNotEqual(response.status_code, 200)

    # ================= PROFILE =================

    def test_profile_page(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    # ================= SUBJECT =================

    def test_subject_access_student(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse("subject_detail", args=["anatomy"]))
        self.assertEqual(response.status_code, 200)

    def test_subject_block_non_student(self):
        self.client.login(username='admin1', password='12345')
        response = self.client.get(reverse("subject_detail", args=["anatomy"]))
        self.assertNotEqual(response.status_code, 200)

    # ================= EXAM NOTICE =================

    def test_exam_notice_visible(self):
        self.client.login(username='student1', password='12345')

        ExamNotice.objects.create(
            exam_type="card",
            course="MBBS",
            phase=1,
            title="Test Notice",
            description="Hello"
        )

        response = self.client.get(reverse('exam_notice', args=['card', 1]))
        self.assertContains(response, "Test Notice")

    def test_exam_notice_hidden_other_course(self):
        self.client.login(username='student1', password='12345')

        ExamNotice.objects.create(
            exam_type="card",
            course="BDS",
            phase=1,
            title="Hidden",
            description="Should not show"
        )

        response = self.client.get(reverse('exam_notice', args=['card', 1]))
        self.assertNotContains(response, "Hidden")

    # ================= ADMIN NOTICE =================

    def test_admin_add_notice(self):
        self.client.login(username='admin1', password='12345')

        response = self.client.post(reverse('add_notice'), {
            "exam_type": "card",
            "course": "MBBS",
            "phase": 1,
            "title": "Admin Notice",
            "description": "Test"
        })

        self.assertEqual(response.status_code, 302)

    def test_student_cannot_add_notice(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse('add_notice'))
        self.assertNotEqual(response.status_code, 200)

    # ================= LIBRARY =================

    def test_book_issue(self):
        book = Book.objects.create(
            title="Test Book",
            author="ABC",
            total_copies=5,
            available_copies=5
        )

        issue = Issue.objects.create(
            student=self.student,
            book=book,
            due_date="2026-05-01"
        )

        self.assertEqual(issue.book.title, "Test Book")

    def test_library_page(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/library/my-books/')
        self.assertEqual(response.status_code, 200)

    # ================= PAYMENT =================

    def test_payment_create(self):
        self.client.login(username='student1', password='12345')

        response = self.client.post(reverse("payment"), {
            "amount": 1000,
            "method": "bkash",
            "purpose": "Exam Fee"
        })

        self.assertEqual(response.status_code, 200)

    # ================= RESULT =================

    def test_result_page(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/result/')
        self.assertEqual(response.status_code, 200)

    # ================= ELIGIBILITY =================

    def test_student_status(self):
        StudentRecord.objects.create(
            user=self.student,
            attendance=80,
            item_pass=True,
            card_pass=True,
            term_pass=False
        )

        self.client.login(username='student1', password='12345')
        response = self.client.get('/student/status/')
        self.assertEqual(response.status_code, 200)

    # ================= DOCTOR =================

    def test_doctor_schedule_access(self):
        self.client.login(username='doctor1', password='12345')
        response = self.client.get('/doctor/schedule/')
        self.assertEqual(response.status_code, 200)