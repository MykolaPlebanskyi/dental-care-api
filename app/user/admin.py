from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_staff']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Особиста інформація', {'fields': ('first_name', 'last_name')}),
        ('Права доступу', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Системне', {'fields': ('must_change_password', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name',
                'role', 'password1', 'password2',
                'is_staff', 'is_superuser'
            ),
        }),
    )

    def change_password(self, request, user_id, form_url=''):
        response = super().change_password(request, user_id, form_url)
        if request.method == 'POST' and response.status_code == 302:
            user = self.get_object(request, user_id)
            if user:
                user.must_change_password = False
                user.save()
        return response
