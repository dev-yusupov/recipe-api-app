"""
    Test cases for the User API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")

def create_user(**params):
    """Create and return a new user."""

    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test the public features of the API."""
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_successful(self):
        """Test creating a user is successful."""
        payload = {
            "email": "test@test.com",
            "password": "testpass123",
            "name": "Test Testov",
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_with_email_exists_error(self):
        """Test error returns when email exists."""
        payload = {
            "email": "test@test.com",
            "password": "testpass123",
            "name": "Test Testov",
        }

        create_user(**payload)
        response = self.client.get(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """Test returns error if password is too short."""
        payload = {
            "email": "test@test.com",
            "password": "pw",
            "name": "Test Testov",
        }
        response = self.client.get(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)