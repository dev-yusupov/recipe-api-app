"""
Test Ingredients APIs
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Ingredient,
)
from recipe.serializers import (
    IngredientSerializer
)

INGREDIENT_URL = reverse("recipe:ingredient-list")

def detail_url(ingredient_id):
    return reverse("recipe:ingredient-detail", args=[ingredient_id])

def create_user(email="test@test.com", password="123test"):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicIngredientsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test auth is required for retrieving ingredients."""
        response = self.client.get(INGREDIENT_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class PrivateIngredientsTests(TestCase):
    """Test authenticated API requests."""
    
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
    
    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name="Test1")
        Ingredient.objects.create(user=self.user, name="Test2")

        response = self.client.get(INGREDIENT_URL)
        
        ingredients = Ingredient.objects.all().order_by("-name")
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_ingredients_limited_user(self):
        user2 = create_user(email="test2@test.com")
        Ingredient.objects.create(user=user2, name="Salt")
        ingredient = Ingredient.objects.create(user=self.user, name="Papper")

        response = self.client.get(INGREDIENT_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)
        self.assertEqual(response.data[0]['id'], ingredient.id)
    
    def test_update_ingredient(self):
        """Test updating ingredients."""
        ingredient = Ingredient.objects.create(user=self.user, name="Apple")

        payload = {
            "name": "Banana",
        }
        url = detail_url(ingredient.id)

        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])
    
    def test_delete_ingredient_url(self):
        """Test deletes the ingredient."""
        ingredient = Ingredient.objects.create(user=self.user, name="Apple")

        url = detail_url(ingredient.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredients.exists())