from django.shortcuts import render
from rest_framework import viewsets, permissions, authentication

from core.models import Recipe
from .serializers import RecipeSerializer, RecipeDetailsSerializer


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
