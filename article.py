# news_analyzer/article.py
from datetime import datetime
from typing import Optional
import google.generativeai as genai     
import os
import requests

class Article:
    """Represents a news article with its metadata and content."""
    
    def __init__(
        self,
        title: str,
        url: str,
        source_name: str,
        publication_date: datetime,
        content: Optional[str] = None,
    ):
        self.title = title
        self.url = url
        self.source_name = source_name
        self.content = content
        self.ai_summary = None
        
        # Handle publication_date conversion
        if isinstance(publication_date, str):
            self.publication_date = datetime.fromisoformat(publication_date.replace('Z', '+00:00'))
        else:
            self.publication_date = publication_date

    def generate_summary(self) -> None:
        """
        Generate an AI summary for the article using Gemini AI.
        Fetches the full article content from the URL before summarizing.
        """
        if not self.url:
            raise ValueError("No URL available to fetch content")

        try:
            # Fetch the full article content
            response = requests.get(self.url)
            response.raise_for_status()
            html_content = response.text

            # Configure Gemini AI
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY not found in environment variables")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            prompt = f"""
            Please provide a concise summary (2-3 sentences) of the following news article. The summary should be in the same language as the article.
            Note: The content provided is in HTML format, so please extract the main article content
            while ignoring navigation menus, ads, and other webpage elements.

            Title: {self.title}
            URL: {self.url}
            HTML Content: {html_content}
            """

            response = model.generate_content(prompt)
            self.ai_summary = response.text

        except requests.exceptions.RequestException as e:
            self.ai_summary = f"Error fetching article content: {str(e)}"
        except Exception as e:
            self.ai_summary = f"Error generating summary: {str(e)}"

    def to_dict(self) -> dict:
        """
        Convert the Article instance to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the Article
        """
        return {
            'title': self.title,
            'url': self.url,
            'source_name': self.source_name,
            'publication_date': self.publication_date.isoformat(),
            'content': self.content,
            'ai_summary': self.ai_summary
        }

    @staticmethod
    def from_dict(data: dict) -> 'Article':
        """
        Create an Article instance from a dictionary.
        
        Args:
            data: Dictionary containing article data
            
        Returns:
            Article: New Article instance
        """
        article = Article(
            title=data['title'],
            url=data['url'],
            source_name=data['source_name'],
            publication_date=data['publication_date'],
            content=data['content']
        )
        article.ai_summary = data.get('ai_summary')
        return article
    