
# news/urls.py

from django.urls import path
from .views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),  # ✅ Added for detail view
]







