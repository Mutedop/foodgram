from rest_framework import mixins, viewsets


class RecipeModelViewSet(
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    pass
