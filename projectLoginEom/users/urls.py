from django.urls import path, include
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    LogoutView,ProtectedView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)



urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="auth_logout"),
    path("protected/", ProtectedView.as_view(), name="protected"),
]
