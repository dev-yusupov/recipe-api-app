"""
Test for the tag API
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Tag,
    Recipe,
    )

from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")

def detail_url(tag_id):
    """Create and return a tag detail url."""
    return reverse("recipe:tag-detail", args=[tag_id])

def create_user(email="test@test.com", password="1234test"):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)

class PublicTagsApiTests(TestCase):
    """Test unauthorized API requests."""

    def setUp(self):
        self.client = APIClient()
    
    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateTagsApiTests(TestCase):
    """Test autherized API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        response = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        user2 = create_user(email="test1@test.com")
        Tag.objects.create(user=user2, name="Fluity")
        tag = Tag.objects.create(user=self.user, name="Fastfood")

        response = self.client.get(TAGS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], tag.name)
        self.assertEqual(response.data[0]["id"], tag.id)
        
    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, name="After dinner")
        
        payload = {
            'name': 'Dessert',
        }
        url = detail_url(tag.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()

        self.assertEqual(tag.name, payload['name'])
    
    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name="Bakery")

        url = detail_url(tag.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())
    
    def test_filter_tags_assigned_to_recipes(self):
        """Test listing ingridients by those assigned to recipes."""
        tag1 = Tag.objects.create(user=self.user, name="Apple")
        tag2 = Tag.objects.create(user=self.user, name="Banana")
        recipe = Recipe.objects.create(
            title="Apple cake",
            time_minutes=5,
            price=Decimal("4.5"),
            user=self.user,
        )
        recipe.tags.add(tag1)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, response.data)
        self.assertNotIn(s2.data, response.data)
    
    def test_filtered_tags_unique(self):
        """Test filtered ingredients returns a unique list."""
        tag = Tag.objects.create(user=self.user, name="Egg")
        Tag.objects.create(user=self.user, name="Lentils")
        recipe1 = Recipe.objects.create(
            title="Egg Benedict", 
            time_minutes=20,
            price=Decimal("20"),
            user=self.user,
        )
        recipe2 = Recipe.objects.create(
            title="Herb Eggs",
            time_minutes=60,
            price=Decimal("4.0"),
            user=self.user,
        )
        recipe1.tags.add(tag)
        recipe2.tags.add(tag)

        response = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(response.data), 1)