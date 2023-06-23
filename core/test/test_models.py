from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import (
    Recipe, 
    Tag,
    Ingredient,
    )

def create_user(email="test@test.com", password="1234test"):
    """Function creates a user."""
    return get_user_model().objects.create_user(email, password)

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test of creating user with email successfully."""
        email = "test@example.com"
        password = "testpass1234"

        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.com", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, excepted in sample_emails:
            user = get_user_model().objects.create_user(email=email, password="1234test")
            self.assertEqual(user.email, excepted)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email and raising error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "testuser")
    
    def test_create_superuser(self):
        """Test creating superuser."""
        user = get_user_model().objects.create_superuser(
            "test@gexample.com",
            "1234test"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        
    
    def test_create_recipe(self):
        """Test creating recipes."""
        user = get_user_model().objects.create_user(
            "test@test.com",
            "1234test",
        )
        recipe = Recipe.objects.create(
            user=user,
            title="Test Recipe title",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample recipe description.",
        )

        self.assertEqual(str(recipe), recipe.title)
    
    def test_create_tag(self):
        """Test createing tag successful."""
        user = create_user()
        tag = Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)
    
    def test_create_ingredient(self):
        """Test creating ingredients."""
        user = create_user()
        ingredient = Ingredient.objects.create(
            user=user,
            name="Test1"
        )

        self.assertEqual(str(ingredient), ingredient.name)
    