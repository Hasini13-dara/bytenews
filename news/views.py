from django.views.generic import ListView, DetailView
from .models import Article

class ArticleListView(ListView):
    model = Article
    template_name = 'home.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = ['-published_date']  # Ensure this matches your model field

    def get_queryset(self):
        # Only return articles that have a non-null published_date
        queryset = super().get_queryset().filter(published_date__isnull=False)

        # Optional: Only show articles with category if category filter is used
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__id=category)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Article.objects.values_list('category', flat=True).distinct()
        context['current_category'] = self.request.GET.get('category')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
