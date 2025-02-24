from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('account', views.UserAccountViewSet, basename='user-account')
router.register('all-users', views.AllUserViewSet, basename='all-users')
router.register('handle-staff', views.UserStaffViewSet, basename='handle-staff')
router.register('admin-messages', views.AdminMessageViewSet, basename='admin-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.UserRegistrationSerializerViewSet.as_view(), name='register'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('update/', views.UserProfileView.as_view(), name='user-update'),
]
