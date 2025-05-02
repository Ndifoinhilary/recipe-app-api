
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


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag object
    """
    class Meta:
        model = models.Tag
        fields = ['id', 'name']
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient object
    """
    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ('id',)


