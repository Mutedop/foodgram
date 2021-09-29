from django_filters.rest_framework import (BooleanFilter,
                                           CharFilter, FilterSet,
                                           AllValuesMultipleFilter)

from .models import Ingredient
from .models import Recipe


class IngredientsFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipesFilter(FilterSet):
    tags = AllValuesMultipleFilter(field_name='tags__slug')
    author = CharFilter(field_name='author__id')
    name = CharFilter(field_name='ingredients__name')
    is_favorited = BooleanFilter(field_name='favorites__recipe')
    is_in_shopping_cart = BooleanFilter(field_name='shop_cart__recipe')

    class Meta:
        model = Recipe
        fields = [
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
        ]

    def filter_favorite(self, queryset, _, value):
        user = self.request.user
        if value is True:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_shopping_cart(self, queryset, _, value):
        user = self.request.user
        if value is True:
            return queryset.filter(shop_cart__user=user)
        return queryset
