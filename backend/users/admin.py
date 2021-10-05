from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Subscription

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name', 'is_staff'
    )
    list_filter = ('email', 'first_name', )
    search_fields = ('email', 'username', )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')
    list_filter = ('user', 'following', )
    search_fields = ('user', 'following', )
    empty_value_display = '-empty-'
