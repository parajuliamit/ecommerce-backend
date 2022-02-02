from django.urls import path
from base.views import user_views as views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.registerUser, name='register'),
    path('profile/update/', views.updateUserProfile, name='user-profile-update'),
    path('profile/', views.getUserProfile, name='user-profile'),
    path('change-password/', views.changePassword, name='change-passwprd'),
]
