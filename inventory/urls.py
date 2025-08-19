from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryChangeLogViewSet, UserViewSet, LoginView

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='item')
router.register(r'changes', InventoryChangeLogViewSet, basename='change')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

]
