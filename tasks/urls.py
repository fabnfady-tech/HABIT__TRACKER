from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'api/tasks',      views.TaskViewSet,     basename='task')
router.register(r'api/categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    # الواجهة
    path('', views.index, name='index'),

    # Auth
    path('api/auth/register/', views.RegisterView.as_view(), name='register'),
    path('api/auth/login/',    views.LoginView.as_view(),    name='login'),
    path('api/auth/logout/',   views.LogoutView.as_view(),   name='logout'),
    path('api/auth/refresh/',  TokenRefreshView.as_view(),   name='token_refresh'),

    # Tasks + Categories (CRUD تلقائي)
    path('', include(router.urls)),
]