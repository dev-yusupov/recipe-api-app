"""
Views for the recipe APIs.
"""
from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet,
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from core.models import (
    Recipe,
    Tag,
    Ingredient,
)
from recipe.serializers import (
    RecipeSerializer, 
    RecipeDetailSerializer, 
    TagSerializer,
    IngredientSerializer,
    RecipeImageSerializer,
)


class RecipeViewSet(ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")
    
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == "list":
            return RecipeSerializer
        elif self.action == "upload_image":
            return RecipeImageSerializer
        
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)
    
    @action(methods=["POST"], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BaseRecipeAttrViewSet(ListModelMixin,
                            GenericViewSet,
                            UpdateModelMixin,
                            DestroyModelMixin):
    """BaseV Viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')

class TagViewSet(BaseRecipeAttrViewSet):
    """Manage tags in database."""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Mapping ingredients in the database."""
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()