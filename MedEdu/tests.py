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

    # ✅ User Created Test
    def test_user_created(self):
        user = User.objects.get(username='student1')
        self.assertEqual(user.role, 'medical_student')

    # ✅ Login Test (using mededu_id)
    def test_login(self):
        response = self.client.post(reverse("login"), {
            "mededu_id": self.user.mededu_id,
            "password": "12345"
        })
        self.assertEqual(response.status_code, 302)  # redirect means success

    # ❌ Invalid Login Test
    def test_invalid_login(self):
        response = self.client.post(reverse("login"), {
            "mededu_id": self.user.mededu_id,
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid")

    # ✅ Dashboard Access Test
    def test_student_dashboard(self):
        self.client.login(username='student1', password='12345')

        response = self.client.get('/student/dashboard/')
        self.assertEqual(response.status_code, 200)

    # 🔥 Extra: Password Reset Test
    def test_reset_password(self):
        response = self.client.post(reverse("forgot_password"), {
            "mededu_id": self.user.mededu_id,
            "new_password": "newpass123",
            "confirm_password": "newpass123"
        })

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newpass123"))

