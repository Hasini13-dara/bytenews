from django.core.management.base import BaseCommand
from news.utils import fetch_news_from_rss, generate_summary
from news.models import Article, Category

class Command(BaseCommand):
    help = 'Scrapes news articles from various RSS feeds and saves them to the database.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting multi-source scraping...")

        sources = {
            "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
            "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
            "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss"
        }

        articles_added = 0
        default_category, _ = Category.objects.get_or_create(name='General')

        for source_name, url in sources.items():
            self.stdout.write(f"Fetching from {source_name}...")
            articles_data = fetch_news_from_rss(url, source_name)

            for article_data in articles_data:
                if not Article.objects.filter(link=article_data['link']).exists():
                    # ✅ Generate summary from content
                    article_summary = generate_summary(article_data['content'])

                    # ✅ Create the article with the summary
                    Article.objects.create(
                        title=article_data['title'],
                        content=article_data['content'],
                        link=article_data['link'],
                        publication_date=article_data['publication_date'],
                        author=article_data.get('author', 'Unknown'),
                        source=article_data['source'],
                        category=default_category,
                        summary=article_summary  # ✅ Save summary
                    )
                    articles_added += 1

        self.stdout.write(self.style.SUCCESS(f"Finished scraping. Added {articles_added} new articles."))
