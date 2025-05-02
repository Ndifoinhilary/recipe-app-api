
from rest_framework import serializers

from core import  models



class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient object
    """
    class Meta:
        model = models.Ingredient
        fields = ['id', 'name']
        read_only_fields = ('id',)

class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag object
    """
    class Meta:
        model = models.Tag
        fields = ['id', 'name']
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Recipe object
    """
    ingredients = IngredientSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = models.Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'ingredients']
        read_only_fields = ('id',)

    def _get_or_crate_tag(self, tags, recipe):
        """
        Crate a tag if it exists
        :param tag:
        :param recipe:
        :return:
        """
        auth_user = self.context['request'].user
        for tag in tags:
            tag_object, created = models.Tag.objects.get_or_create(user=auth_user, *tag)
            recipe.tag.add(tag_object)

    def _get_or_crate_ingredients(self, ingredients, recipe):
        """
        Crate ingredients if it exists
        :param ingredients:
        :param recipe:
        :return:
        """
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_object, created = models.Ingredient.objects.get_or_create(user=auth_user, **ingredient)
            recipe.ingredients.add(ingredient_object)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients', [])
        tags = validated_data.pop('tags', [])
        recipe = models.Recipe.objects.create(**validated_data)
        self._get_or_crate_ingredients(ingredients, recipe)
        self._get_or_crate_tag(tags, recipe)
        return recipe

class RecipeDetailsSerializer(RecipeSerializer):
    """
    Serializer for the Recipe object
    """
    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']





