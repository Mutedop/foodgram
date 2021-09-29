from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .filters import IngredientsFilter
from .filters import RecipesFilter
from .models import Ingredient, Tag, Recipe, Favorite, RecipeIngredients
from .paginators import PageNumberPaginatorModified
from .permissions import IsAuthorOrAdmin
from .serializers import (IngredientsSerializer, TagsSerializer,
                          RecipeSerializer, CreateRecipeSerializer,
                          FavouriteSerializer, ShoppingCartSerializer)


class RetrieveAndListViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass


class IngredientsViewSet(RetrieveAndListViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagsViewSet(RetrieveAndListViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter
    pagination_class = PageNumberPaginatorModified

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthenticated])
    def favorite(self, request, recipe_id):
        data = {
            'user': request.user.id,
            'recipe': recipe_id
        }
        serializer = FavouriteSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, recipe_id):
        data = {
            'user': request.user.id,
            'recipe': recipe_id
        }
        serializer = ShoppingCartSerializer(
            data=data,
            context={
                'request': request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=recipe_id)
        shopping_list = get_object_or_404(
            ShoppingCartSerializer,
            user=user,
            recipe=recipe
        )
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = user.purchases.all()
        ingredients_list = {}
        for item in shopping_cart:
            recipe = item.recipe
            ingredients = RecipeIngredients.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in ingredients_list:
                    ingredients_list[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                    }
                else:
                    ingredients_list[name]['amount'] += amount

        shopping_list = []
        for item in ingredients_list:
            shopping_list.append(
                f'{item} - {ingredients_list[item]["amount"]} '
                f'{ingredients_list[item]["measurement_unit"]} \n'
            )
        response = HttpResponse(shopping_list, 'Content-Type: text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.txt"')
        return response
