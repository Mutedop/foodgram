from django_filters.rest_framework import (BooleanFilter,
                                           CharFilter, FilterSet,
                                           AllValuesMultipleFilter)

from .models import Ingredient
from .models import Recipe


class IngredientsFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipesFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug', label='Tags')
    is_favorited = BooleanFilter(method='get_favorite', label='Favorited')
    is_in_shopping_cart = BooleanFilter(
        method='get_shopping',
        label='In shopping cart'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'author', 'tags', 'is_in_shopping_cart')

    def get_favorite(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(in_favorite__user=self.request.user)
        return Recipe.objects.all()

    def get_shopping(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shoppingcart__user=self.request.user)
        return Recipe.objects.all()
