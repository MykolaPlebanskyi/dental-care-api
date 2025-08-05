"""
Serializers for the user API View.
"""
from rest_framework import serializers
from .models import User, Dentist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data, role=User.ROLES.PATIENT)
        user.set_password(password)
        user.save()
        return user

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class DentistCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    specialization = serializers.ChoiceField(choices=Dentist.SPECIALIZATIONS)
    biography = serializers.CharField(required=False)
    photo = serializers.ImageField(required=False)

    def generate_unique_email(self, first_name, last_name):
        domain = "clinic.com"
        base_email = f"{last_name.lower()}.{first_name.lower()}@{domain}"
        email = base_email
        counter = 1
        while User.objects.filter(email=email).exists():
            email = f"{last_name.lower()}.{first_name.lower()}{counter}@{domain}"
            counter += 1
        return email

    def create(self, validated_data):
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = self.generate_unique_email(first_name, last_name)

        user = User.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=User.ROLES.DENTIST,
        )

        dentist = Dentist.objects.create(user=user, **validated_data)
        return dentist