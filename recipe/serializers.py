"""
Serializers for Recipe APIs
"""
from rest_framework.serializers import ModelSerializer

from core.models import Recipe, Tag

class RecipeSerializer(ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link"]
        read_only_fields = ["id"]

class RecipeDetailSerializer(RecipeSerializer):
    """Recipe detail serializers."""
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']

class TagSerializer(ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
        