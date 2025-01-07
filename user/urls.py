from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserLoginViewSet,UserRegisterViewSet,UserLogoutViewSet,TokenRefreshViewSet

router = DefaultRouter()
router.register('register', UserRegisterViewSet, basename='user-register')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginViewSet.as_view(), name='user-login'),
    path('logout/', UserLogoutViewSet.as_view(), name='user-logout'),
    path('token/refresh/',TokenRefreshViewSet.as_view(), name='token-refresh'),
    
]