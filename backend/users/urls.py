from django.urls import path, include
from djoser import views
from .views import SubscriptionApiView, ListSubscriptionViewSet

urlpatterns = [
    path('', include('djoser.urls')),
    path('users/subscriptions/',
         ListSubscriptionViewSet.as_view(),
         name='subscription'),
    path('users/<int:id>/subscribe/',
         SubscriptionApiView.as_view(),
         name='subscribe'),
    path('auth/token/login/',
         views.TokenCreateView.as_view(),
         name='login'),
    path('auth/token/logout/',
         views.TokenDestroyView.as_view(),
         name='logout'),
]
