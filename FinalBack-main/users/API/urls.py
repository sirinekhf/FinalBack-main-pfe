from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenRefreshView)

from .views import MyTokenObtainPairView

urlpatterns = [
    path('',views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view()), #return a token and refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]