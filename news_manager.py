# news_analyzer/news_manager.py
import json
import time
from typing import List, Optional
import requests
from article import Article

class NewsManager:
    
    def __init__(self, news_api_key: str):

        self.news_api_key = news_api_key
        self.articles: List[Article] = []
        self.news_api_base_url = "https://newsapi.org/v2/everything"

    def fetch_articles(
        self, 
        params: dict
    ) -> List[Article]:
        print(f"Fetching articles for query: {params['q']}")
        params['apiKey'] = self.news_api_key
        try:
            response = requests.get(self.news_api_base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Process articles
            new_articles = []
            for article_data in data.get('articles', []):
                article = Article(
                    title=article_data.get('title', ''),
                    url=article_data.get('url', ''),
                    source_name=article_data.get('source', {}).get('name', 'Unknown'),
                    publication_date=article_data.get('publishedAt', ''),
                    content=article_data.get('content', article_data.get('description', ''))
                )
                new_articles.append(article)
            
            self.articles.extend(new_articles)
            print(f"Successfully fetched {len(new_articles)} articles")
            return new_articles
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch articles: {e}")

    def batch_summarize(self, delay: float = 1.0) -> None:
        print("Starting batch summarization")
        print(f"{len(self.articles)} to be summarized")
        for i, article in enumerate(self.articles):
            if not article.ai_summary:
                try:
                    article.generate_summary()
                    print(f"{i+1}/{len(self.articles)} COMPLETED")
                    time.sleep(delay)  # Rate limiting
                except Exception as e:
                    print(f"Failed to generate summary for article '{article.title}': {e}")
                
        print("Completed batch summarization")

    def save_to_file(self, filename: str) -> None:

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(
                    [article.to_dict() for article in self.articles],
                    f,
                    indent=2,
                    ensure_ascii=False
                )
            print(f"Successfully saved {len(self.articles)} articles to {filename}")
            
        except Exception as e:
            print(f"Failed to save articles to {filename}: {e}")
            raise

    def load_from_file(self, filename: str) -> None:

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.articles = [Article.from_dict(article_data) for article_data in data]
            print(f"Successfully loaded {len(self.articles)} articles from {filename}")
            
        except Exception as e:
            print(f"Failed to load articles from {filename}: {e}")
            raise