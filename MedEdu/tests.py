from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class MedEduTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='student1',
            password='12345',
            role='medical_student'
        )

    # ✅ Signup / User Create Test
    def test_user_created(self):
        user = User.objects.get(username='student1')
        self.assertEqual(user.role, 'medical_student')

    # ✅ Login Test
    def test_login(self):
        login = self.client.login(username='student1', password='12345')
        self.assertTrue(login)

    # ❌ Wrong Login Test
    def test_invalid_login(self):
        login = self.client.login(username='student1', password='wrong')
        self.assertFalse(login)

    # ✅ Role-based Dashboard Test
    def test_student_dashboard(self):
        self.client.login(username='student1', password='12345')
        response = self.client.get('/student/dashboard/')
        self.assertEqual(response.status_code, 200)