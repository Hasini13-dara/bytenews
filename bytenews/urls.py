from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from news.views import landing_page, ArticleViewSet  # ✅ Imported ArticleViewSet for API
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers  # ✅ Imported DRF router
from news.views import ArticleViewSet, UserPreferenceViewSet
from news.views import CategoryViewSet, ArticleViewSet, UserPreferenceViewSet
# ✅ DRF router setup
router = routers.DefaultRouter()
router.register(r'articles', ArticleViewSet)  # API at /api/articles/
router.register(r'preferences', UserPreferenceViewSet)  # ✅ Register the route
router.register(r'categories', CategoryViewSet)
  # ✅ Import this view
from news.views import GenerateAudioAPIView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    # ✅ Home page goes to landing page
    path('', landing_page, name='landing'),

    # ✅ Article list at /articles/
    path('articles/', include('news.urls')),

    # ✅ Auth routes
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('logged_out/', TemplateView.as_view(template_name='registration/logged_out.html')),
    path('api/articles/<int:pk>/generate_audio/', GenerateAudioAPIView.as_view(), name='api_generate_audio'),
    # ✅ API routes
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)