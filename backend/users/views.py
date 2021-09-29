from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Subscription
from .serializers import SubscriptionSerializer, ShowSubscriptionSerializer

User = get_user_model()


class SubscriptionApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        data = {
            'user': request.user.id,
            'following': id
        }
        serializer = SubscriptionSerializer(
            data=data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        subscription = get_object_or_404(
            Subscription,
            user=user,
            following=following
        )
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListSubscriptionViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ShowSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)
