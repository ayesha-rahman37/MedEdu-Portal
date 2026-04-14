from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

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
        self.assertContains(response, "Invalid")

    # ================= DASHBOARD =================

    def test_student_dashboard(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/student/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_without_login(self):
        response = self.client.get('/student/dashboard/')
        self.assertNotEqual(response.status_code, 200)

    def test_dashboard_redirect(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    # ================= PROFILE =================

    def test_profile_access(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        self.client.login(username='student1', password='12345')

        response = self.client.post(reverse('edit_profile'), {
            # file optional
        })

        self.assertEqual(response.status_code, 302)

    # ================= PASSWORD RESET =================

    def test_reset_password(self):
        response = self.client.post(reverse("forgot_password"), {
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

        self.assertContains(response, "match")

# ================= SUBJECT =================

def test_subject_detail_page(self):
    from .models import Subject

    subject = Subject.objects.create(
        name="Anatomy",
        slug="anatomy"
    )

    self.client.login(username='student1', password='12345')

    response = self.client.get(reverse("subject_detail", args=["anatomy"]))

    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Syllabus")


def test_subject_requires_login(self):
    from .models import Subject

    Subject.objects.create(name="Anatomy", slug="anatomy")

    response = self.client.get(reverse("subject_detail", args=["anatomy"]))

    # should redirect (login required)
    self.assertNotEqual(response.status_code, 200)


# ================= ROLE BASED =================

def test_medical_student_access(self):
    self.client.login(username='student1', password='12345')

    response = self.client.get('/student/dashboard/')
    self.assertEqual(response.status_code, 200)


def test_dental_student_access(self):
    dental_user = User.objects.create(
        username='dental1',
        role='dental_student',
        is_verified=True
    )
    dental_user.set_password('12345')
    dental_user.save()

    self.client.login(username='dental1', password='12345')

    response = self.client.get('/student/dashboard/')
    self.assertEqual(response.status_code, 200)


# ================= PDF LOGIC =================

def test_pdf_load(self):
    from .models import Subject

    Subject.objects.create(name="Anatomy", slug="anatomy")

    self.client.login(username='student1', password='12345')

    response = self.client.get(reverse("subject_detail", args=["anatomy"]))

    # check PDF path exists in response
    self.assertContains(response, "/static/pdfs/")