from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema

from . import views

app_name = 'students_api'

# Принудительно вешаем тэг 'Students' на сторонние View из SimpleJWT
TokenObtainPairView = extend_schema_view(post=extend_schema(tags=['Students']))(TokenObtainPairView)
TokenRefreshView = extend_schema_view(post=extend_schema(tags=['Students']))(TokenRefreshView)

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]