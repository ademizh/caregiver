from django.test import TestCase
from .models import User

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            email="test@example.com",
            given_name="Test",
            surname="User",
            city="Test City",
            password="testpass"
        )
        self.assertEqual(user.email, "test@example.com")