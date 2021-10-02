from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.serializers import CustomUserSerializer
from .fields import Base64ImageField
from .models import (Ingredient, Tag, RecipeIngredients,
                     Recipe, Favorite, ShoppingCart)

User = get_user_model()


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name', 'measurement_unit']


class AddIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredients
        fields = ['id', 'amount']


class ShowRecipeIngredientsSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredients
        fields = ['id', 'name', 'measurement_unit', 'amount']


class ShowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'image', 'cooking_time']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time',
            'is_favorited', 'is_in_shopping_cart'
        )

    def get_ingredients(self, obj):
        ingredients = RecipeIngredients.objects.filter(recipe=obj)
        return ShowRecipeIngredientsSerializer(
            ingredients,
            many=True
        ).data

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Favorite.objects.filter(
            user=request.user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            user=request.user,
            recipe=obj,
        ).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None, use_url=True, required=False)
    author = CustomUserSerializer(read_only=True)
    ingredients = AddIngredientsSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'name',
                  'image', 'text', 'cooking_time']

    def add_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = ingredient['amount']
            ingredient_id = ingredient['id']
            if RecipeIngredients.objects.filter(
                    recipe=recipe,
                    ingredient=ingredient_id
            ).exists():
                amount += 1
            RecipeIngredients.objects.update_or_create(
                recipe=recipe,
                ingredient=ingredient_id,
                defaults={
                    'amount': amount
                })

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if ingredients == [None]:
            raise ValidationError('Из солнечной энергии, готовить будем мы?')
        for ingredient in ingredients:
            if int(ingredient['amount']) <= 0:
                raise ValidationError('Достать обратно?')
        return data

    def create(self, validated_data):
        author = self.context.get('request').user
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_recipe_ingredients(ingredients_data, recipe)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.cooking_time = validated_data.get(
            'cooking_time',
            recipe.cooking_time
        )

        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            self.add_recipe_ingredients(ingredients, recipe)
        if 'tags' in self.initial_data:
            tags_data = validated_data.pop('tags')
            recipe.tags.set(tags_data)
        recipe.save()
        return recipe

    def to_representation(self, recipe):
        data = ShowRecipeSerializer(
            recipe,
            context={
                'request': self.context.get('request')
            }
        ).data
        return data


class FavouriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if Favorite.objects.filter(
                user=user,
                recipe__id=recipe_id
        ).exists():
            raise ValidationError('^ Есть такой рецепт ^')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {
            'request': request
        }
        return ShowRecipeSerializer(
            instance.recipe, context=context
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )

    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipe']

    def validate(self, data):
        user = data['user']
        recipe_id = data['recipe'].id
        if ShoppingCart.objects.filter(
                user=user,
                recipe__id=recipe_id
        ).exists():
            raise ValidationError('$ Уже добавлен в покупки $')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {
            'request': request
        }
        return ShowRecipeSerializer(
            instance.recipe,
            context=context
        ).data
