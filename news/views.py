from django.views.generic import ListView, DetailView
from django.db.models import Count, Q
from .models import Article, Category

class ArticleListView(ListView):
    model = Article
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        queryset = Article.objects.all().order_by('-published_date')
        category = self.request.GET.get('category')
        query = self.request.GET.get('q')

        # If a category is selected via button/filter
        if category:
            queryset = queryset.filter(category__name=category)
        
        # If a search is performed via input box
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(summary__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()  # Prevent duplicates if multiple conditions match

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.annotate(article_count=Count('article'))
        context['categories'] = categories
        context['current_category'] = self.request.GET.get('category')
        context['query'] = self.request.GET.get('q', '')
        return context

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
