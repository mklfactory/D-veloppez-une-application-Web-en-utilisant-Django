from django.urls import path
from . import views

urlpatterns = [
# page d'accueil
    path('', views.home, name='home'),  
    path('feed/', views.feed, name='feed'),
# Authentification
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]