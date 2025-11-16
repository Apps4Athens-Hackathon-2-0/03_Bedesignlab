import requests
import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def fetch_top_news(num_articles=3):
    """Fetch top news headlines"""
    # url = f"https://newsapi.org/v2/top-headlines"
    # params = {
    #     "apiKey": NEWS_API_KEY,
    #     "language": "en",
    #     "pageSize": num_articles
    # }
    
    # try:
    #     response = requests.get(url, params=params)
    #     response.raise_for_status()
    #     data = response.json()
        
    #     articles = data.get("articles", [])
        
    #     # Format news for story generation
    #     news_summaries = []
    #     for i, article in enumerate(articles, 1):
    #         summary = f"{i}. {article['title']}: {article.get('description', 'No description')}"
    #         news_summaries.append(summary)
        
    #     return "\n".join(news_summaries)
    
    # except Exception as e:
    #     print(f"Error fetching news: {e}")
    #     return "A collision on Wednesday afternoon involving a bus and another vehicle on Syggrou Avenue has left six people injured but not in danger. Traffic delays continue."
    return "A collision on Wednesday afternoon involving a bus and another vehicle on Syggrou Avenue has left six people injured but not in danger. Traffic delays continue."

# Test it
if __name__ == "__main__":
    print(fetch_top_news())