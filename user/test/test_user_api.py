"""
    Test cases for the User API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")

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
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_password_too_short_error(self):
        """Test returns error if password is too short."""
        payload = {
            "email": "test@test.com",
            "password": "pw",
            "name": "Test Testov",
        }
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload["email"]
        ).exists()
        self.assertFalse(user_exists)
    
    def test_create_token_for_user(self):
        """Test generating token for valid user."""
        user_details = {
            "name": "Test Testov",
            "email": "test@example.com",
            "password": "test-user-password-123"
        }
        create_user(**user_details)

        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_token_credentials(self):
        """Test returns error if credential invalid."""
        create_user(email="test@test.com", password="test1234")

        payload = {"email": "test@test.com", "password": "badpass"}

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_blank(self):
        """Test posting a blank password returns an error."""
        payload = {
            "email": "test@test.com",
            "password": "",
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)