from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        max_length=200, unique=True, blank=False, null=False,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7, unique=True, blank=False, null=False,
        verbose_name='Цвет'
    )
    slug = models.CharField(
        max_length=200, unique=True, blank=False, null=False,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, blank=False, null=False,
        verbose_name='Название'
    )
    measurement_unit = models.CharField(
        max_length=200, blank=False, null=False,
        verbose_name='Единицы измерения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags_recipes',
        verbose_name='Список тегов'
    )
    image = models.ImageField(
        upload_to='recipes/',
        blank=False, null=False,
        verbose_name='Картинка'
    )
    name = models.CharField(
        max_length=200,
        blank=False, null=False,
        verbose_name='Название'
    )
    text = models.TextField(
        blank=False, null=False,
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
                    validators=[MinValueValidator(1)],
                    verbose_name='Время приготовления (в минутах)')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        verbose_name='Список ингредиентов'
    )
    amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Количество'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='unique_recipe_ingredient'
        )]


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite_subscriber',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite_recipe'
        )]
        ordering = ('-id',)
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='Рецепт',
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'user'],
            name='unique_shopping_cart'
        )]
