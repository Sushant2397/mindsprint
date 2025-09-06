from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'splits', views.ExpenseSplitViewSet)

urlpatterns = [
    path('', include(router.urls)),
]