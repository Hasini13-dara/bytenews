# users/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import ArticleListView, ArticleDetailView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.ArticleListView.as_view(), name='home'),  # ✅ Use class-based view
    path('', ArticleListView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'), 
]






