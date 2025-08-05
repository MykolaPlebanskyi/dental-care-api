from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Dentist
from django import forms

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

class DentistAdminForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = Dentist
        fields = ['first_name', 'last_name', 'specialization', 'biography', 'photo']

    def generate_unique_email(self, first_name, last_name):
        domain = "clinic.com"
        base_email = f"{last_name.lower()}.{first_name.lower()}@{domain}"
        email = base_email
        counter = 1
        while User.objects.filter(email=email).exists():
            email = f"{last_name.lower()}.{first_name.lower()}{counter}@{domain}"
            counter += 1
        return email

    def save(self, commit=True):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        email = self.generate_unique_email(first_name, last_name)

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=User.ROLES.DENTIST
        )

        dentist = super().save(commit=False)
        dentist.user = user

        if commit:
            dentist.save()

        return dentist


@admin.register(Dentist)
class DentistAdmin(admin.ModelAdmin):
    form = DentistAdminForm
    list_display = ['user', 'specialization']
    search_fields = ['user__first_name', 'user__last_name', 'specialization']
