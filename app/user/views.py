"""
User views for registration, login, and logout functionality.
"""
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Dentist
from .serializers import UserSerializer, RegisterSerializer, LogoutSerializer, DentistCreateSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Успішний вихід."})
        except Exception:
            return Response({"error": "Помилка виходу."}, status=400)

class DentistCreateAPIView(generics.CreateAPIView):
    queryset = Dentist.objects.all()
    serializer_class = DentistCreateSerializer
    permission_classes = [permissions.IsAdminUser]