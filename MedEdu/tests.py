from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ExamNotice, Book, Issue, Subject

User = get_user_model()


class MedEduTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='student1',
            role='medical_student',
            is_verified=True
        )
        self.user.set_password('12345')
        self.user.save()

    # ================= BASIC =================

    def test_user_created(self):
        user = User.objects.get(username='student1')
        self.assertEqual(user.role, 'medical_student')

    def test_password_check(self):
        self.assertTrue(self.user.check_password("12345"))

    def test_wrong_password(self):
        self.assertFalse(self.user.check_password("wrong"))

    # ================= LOGIN =================

    def test_login(self):
        response = self.client.post(reverse("login"), {
            "mededu_id": self.user.mededu_id,
            "password": "12345"
        })
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        response = self.client.post(reverse("login"), {
            "mededu_id": self.user.mededu_id,
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 200)

    # ================= DASHBOARD =================

    def test_student_dashboard(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/student/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_without_login(self):
        response = self.client.get('/student/dashboard/')
        self.assertNotEqual(response.status_code, 200)

    # ================= PROFILE =================

    def test_profile_access(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        self.client.login(username='student1', password='12345')
        response = self.client.post(reverse('edit_profile'), {})
        self.assertEqual(response.status_code, 302)

    # ================= PASSWORD RESET =================

    def test_reset_password(self):
        self.client.post(reverse("forgot_password"), {
            "mededu_id": self.user.mededu_id,
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))

    def test_reset_password_mismatch(self):
        response = self.client.post(reverse("forgot_password"), {
            "mededu_id": self.user.mededu_id,
            "new_password": "abc123",
            "confirm_password": "wrong"
        })
        self.assertEqual(response.status_code, 200)

    # ================= SUBJECT =================

    def test_subject_detail_page(self):
        Subject.objects.create(
            name="Anatomy",
            slug="anatomy",
            phase=1,
            course_type="MBBS"
        )

        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse("subject_detail", args=["anatomy"]))

        self.assertEqual(response.status_code, 200)

    def test_subject_requires_login(self):
        Subject.objects.create(
            name="Anatomy",
            slug="anatomy",
            phase=1,
            course_type="MBBS"
        )

        response = self.client.get(reverse("subject_detail", args=["anatomy"]))
        self.assertNotEqual(response.status_code, 200)

    # ================= ROLE BASED =================

    def test_dental_student_access(self):
        dental = User.objects.create(
            username='dental1',
            role='dental_student',
            is_verified=True
        )
        dental.set_password('12345')
        dental.save()

        self.client.login(username='dental1', password='12345')
        response = self.client.get('/student/dashboard/')
        self.assertEqual(response.status_code, 200)

    # ================= PDF =================

    def test_pdf_load(self):
        Subject.objects.create(
            name="Anatomy",
            slug="anatomy",
            phase=1,
            course_type="MBBS"
        )

        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse("subject_detail", args=["anatomy"]))

        self.assertEqual(response.status_code, 200)

    # ================= EXAM NOTICE =================

    def test_exam_notice(self):
        self.client.login(username='student1', password='12345')

        ExamNotice.objects.create(
            exam_type="card",
            course="MBBS",
            phase=1,
            title="Test Notice",
            description="Hello"
        )

        response = self.client.get(reverse('exam_notice', args=['card', 1]))
        self.assertEqual(response.status_code, 200)

    def test_exam_notice_filter(self):
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
        admin = User.objects.create(
            username='admin1',
            role='admin',
            is_verified=True
        )
        admin.set_password('12345')
        admin.save()

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

    # ================= ITEM PDF =================

    def test_item_pdf(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get(reverse('item_pdf', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_item_pdf_without_login(self):
        response = self.client.get(reverse('item_pdf', args=[1]))
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
            student=self.user,
            book=book,
            due_date="2026-05-01"
        )

        self.assertEqual(issue.book.title, "Test Book")

    def test_library_page(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/library/my-books/')
        self.assertEqual(response.status_code, 200)

    # ================= RESULT =================

    def test_result_page(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/result/')
        self.assertEqual(response.status_code, 200)