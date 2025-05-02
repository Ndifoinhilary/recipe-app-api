from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication, mixins

from core.models import Recipe, Tag, Ingredient
from .serializers import RecipeSerializer, RecipeDetailsSerializer, TagSerializer, IngredientSerializer


# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        :return:
        """
        if self.action == 'list':
            serializer_class = RecipeSerializer
            return serializer_class
        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new `Recipe` instance.
        :param serializer:
        :return:
        """
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    Tag ApI view
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        """
        Create a new `Tag` instance.
        :param serializer:
        :return:
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Return appropriate tag queryset.
        :return:
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')



class IngredientViewSet(mixins.ListModelMixin,mixins.RetrieveModelMixin,  viewsets.GenericViewSet):
    """
    Ingredient ApI view
    """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


    def get_queryset(self):
        """
        Return appropriate ingredient queryset.
        :return:
        """
        return self.queryset.filter(user=self.request.user).order_by('-name')