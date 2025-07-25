from django.urls import path
from .views import ArticleListView, ArticleDetailView
from . import views



urlpatterns = [
    path('', ArticleListView.as_view(), name='home'),
    path('<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('history/', views.reading_history, name='reading_history'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('generate-summary/<int:pk>/', views.generate_summary_view, name='generate_summary'),  # ✅ Added
    path('article/<int:pk>/generate_summary/', views.generate_summary_view, name='generate_summary'),

]