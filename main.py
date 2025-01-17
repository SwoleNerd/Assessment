import os
import argparse
from dotenv import load_dotenv
from news_manager import NewsManager

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', type=str, default="tech")
    args = parser.parse_args()

    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    news_api_key = os.getenv('NEWS_API_KEY')
    if not news_api_key:
        raise ValueError("NEWS_API_KEY not found in environment variables")

    # Initialize NewsManager
    news_manager = NewsManager(news_api_key)

    try:
        print(f"\nFetching articles about '{args.query}'...")
        params = {
            'q': args.query,  # Keywords or phrases to search for in the article title and body
            'pageSize': 5,
            'from':'2025-01-01',
            'to_date':'2025-01-31',
            'language':'pt',
            'domains':'tecmundo.com.br'

        }
        articles = news_manager.fetch_articles(params)

        if not articles:
            print("No articles found matching your criteria.")
            return

        # Generate summaries
        print("\nGenerating AI summaries...")
        news_manager.batch_summarize()

        # Print results
        print(f"\nFound {len(articles)} articles:\n")

        # Save articles to file
        output_file = "articles.json"
        news_manager.save_to_file(output_file)
        print(f"Articles saved to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main() 