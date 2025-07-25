import nltk
import feedparser
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import string
from email.utils import parsedate_to_datetime

# Ensure NLTK data is available
nltk.download('punkt')
nltk.download('stopwords')

def generate_summary(text, article_title="", num_sentences=3):
    if not text or not isinstance(text, str):
        return "No content available to summarize."

    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english') + list(string.punctuation))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    word_frequencies = Counter(filtered_words)

    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        for word in word_tokenize(sentence.lower()):
            if word in word_frequencies:
                sentence_scores[i] = sentence_scores.get(i, 0) + word_frequencies[word]

    top_indices = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    final_summary = [sentences[i] for i in sorted(top_indices)]

    return " ".join(final_summary)

def fetch_news_from_rss(url, source_name):
    feed = feedparser.parse(url)
    articles = []

    for entry in feed.entries:
        content = entry.get('summary', '')
        article = {
            'title': entry.title,
            'link': entry.link,
            'publication_date': parsedate_to_datetime(entry.published) if 'published' in entry else None,
            'content': content,
            'source': source_name,
            'author': entry.get('author', 'Unknown'),
        }
        articles.append(article)

    return articles
