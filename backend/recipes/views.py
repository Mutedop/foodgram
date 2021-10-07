from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response

from project.paginators import PageNumberPaginatorModified
from .filters import IngredientsFilter
from .filters import RecipesFilter
from .models import (Ingredient, Tag, Recipe, Favorite,
                     RecipeIngredient, ShoppingCart)
from .permissions import IsAuthorOrAdmin
from .serializers import (IngredientsSerializer, TagsSerializer,
                          RecipeSerializer, CreateRecipeSerializer,
                          FavouriteSerializer, ShoppingCartSerializer)
from .viewsets import RecipeModelViewSet


class TagsViewSet(RecipeModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AllowAny, )
    pagination_class = None


class IngredientsViewSet(RecipeModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (AllowAny, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthorOrAdmin, )
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipesFilter
    pagination_class = PageNumberPaginatorModified

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def favorite(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
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
    def delete_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite = get_object_or_404(
            Favorite,
            user=user,
            recipe=recipe
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthorOrAdmin])
    def shopping_cart(self, request, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
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
    def delete_shopping_cart(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        ingredients = ShoppingCart.objects.filter(user=request.user).values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit'
        ).annotate(total=Sum('recipe__recipe_ingredient__amount'))
        ingredients_list = {}
        for ingredient in ingredients:
            name = ingredient['recipe__ingredients__name']
            measurement_unit = ingredient[
                'recipe__ingredients__measurement_unit'
            ]
            amount = ingredient['total']
            ingredients_list[name] = {
                'measurement_unit': measurement_unit,
                'amount': amount
            }
        shopping_cart = []
        for item in ingredients_list:
            shopping_cart.append(
                f'{item} - {ingredients_list[item]["amount"]} '
                f'{ingredients_list[item]["measurement_unit"]} \n'
            )
        response = HttpResponse(shopping_cart, 'Content-Type: text/plain')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="Список покупок.txt"')
        return response
