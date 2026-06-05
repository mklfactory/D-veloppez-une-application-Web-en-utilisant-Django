from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from litrevu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('feed/', views.feed, name='feed'),
    path('ticket/add/', views.create_ticket, name='create_ticket'),
    path('review/add/', views.create_review_no_ticket, name='create_review'),
    path('review/reply/<int:ticket_id>/', views.reply_to_ticket, name='reply_to_ticket'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('posts/', views.my_posts, name='my_posts'),
    path('', views.feed, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)