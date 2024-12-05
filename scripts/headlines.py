import requests
from bs4 import BeautifulSoup

def fetch_headlines(url):
    """
    Fetches the latest news headlines from the given URL.
    """
    try:
        # Send a GET request to the website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad HTTP responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract headlines (update selector based on the website structure)
        headlines = soup.select("h3")  # Assuming headlines are in <h3> tags

        print("\nLatest News Headlines:")
        for i, headline in enumerate(headlines[:10], start=1):  # Limit to top 10
            print(f"{i}. {headline.get_text(strip=True)}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def main():
    """
    Main function to fetch and display headlines.
    """
    url = "https://www.bbc.com/news"  # Replace with the URL of your choice
    fetch_headlines(url)

if __name__ == "__main__":
    main()