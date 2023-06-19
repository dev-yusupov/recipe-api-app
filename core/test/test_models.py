from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test of creating user with email successfully."""
        email = "test@example.com"
        password = "testpass1234"

        user = get_user_model().objects.create(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertEqual(user.password, password)
    
    # def test_new_user_email_normalized(self):
    #     """Test email is normalized for new users."""
    #     sample_emails = [
    #         ["test1@EXAMPLE.com", "test1@example.com"],
    #         ["Test2@Example.com", "Test2@example.com"],
    #         ["TEST3@EXAMPLE.com", "TEST3@example.com"],
    #         ["test4@example.COM", "test4@example.com"],
    #     ]

    #     for email, excepted in sample_emails:
    #         user = get_user_model().objects.create(email=email, password="sample123")
    #         self.assertEqual(user.email, excepted)