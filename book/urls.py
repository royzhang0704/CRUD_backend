from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import BookAPI
router=DefaultRouter()
router.register('books',BookAPI,basename="book") #books API的CRUD

urlpatterns = [
    # 需要是一個列表
    path('', include(router.urls)),
]
