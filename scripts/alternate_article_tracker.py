import requests
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud

API_URL = "https://en.wikipedia.org/w/api.php"

# Function to fetch a random article title
def get_random_article_title():
    params = {
        "action": "query",
        "list": "random",
        "rnnamespace": 0,  # Only main namespace (articles)
        "rnlimit": 1,
        "format": "json"
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        title = data["query"]["random"][0]["title"]
        print(f"Randomly selected article: {title}")
        return title
    else:
        print("Failed to fetch a random article.")
        return None

# Function to fetch page views
def fetch_page_views(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageviews",
        "titles": title,
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            pageviews = page_data.get("pageviews", {})
            return pageviews
    else:
        print("Failed to fetch page views.")
        return {}

# Function to fetch article content
def fetch_article_content(title):
    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "explaintext": True,
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            return page_data.get("extract", "")
    else:
        print("Failed to fetch article content.")
        return ""

# Function to create a word cloud
def create_word_cloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    os.makedirs("results", exist_ok=True)
    output_path = f"results/{title.replace(' ', '_')}_wordcloud.png"
    wordcloud.to_file(output_path)
    print(f"Word cloud saved to {output_path}")

# Function to plot page views
def plot_page_views(pageviews, title):
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in pageviews.keys() if pageviews[date] is not None]
    views = [pageviews[date] for date in pageviews.keys() if pageviews[date] is not None]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, views, marker="o")
    plt.title(f"Page Views for {title}")
    plt.xlabel("Date")
    plt.ylabel("Views")
    plt.grid(True)
    os.makedirs("results", exist_ok=True)
    output_path = f"results/{title.replace(' ', '_')}_pageviews.png"
    plt.savefig(output_path)
    plt.close()
    print(f"Page views plot saved to {output_path}")

# Main function
if __name__ == "__main__":
    # Fetch a random article
    article_title = get_random_article_title()
    if not article_title:
        print("No article selected. Exiting.")
        exit()

    # Fetch and visualize page views
    pageviews = fetch_page_views(article_title)
    if pageviews:
        plot_page_views(pageviews, article_title)
    else:
        print("No page views data available.")

    # Fetch article content and create a word cloud
    article_content = fetch_article_content(article_title)
    if article_content:
        create_word_cloud(article_content, article_title)
    else:
        print("No article content available.")