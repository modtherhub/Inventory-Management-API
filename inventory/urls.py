from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryChangeLogViewSet, UserViewSet, LoginView, UserRegisterView

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='item')
router.register(r'changes', InventoryChangeLogViewSet, basename='change')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

    path('register/', UserRegisterView.as_view(), name='user-register'),
]
