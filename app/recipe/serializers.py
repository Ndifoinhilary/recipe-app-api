
from rest_framework import serializers

from core import  models


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe object
    """
    class Meta:
        model = models.Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ('id',)

class RecipeDetailsSerializer(RecipeSerializer):
    """
    Serializer for the Recipe object
    """
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
