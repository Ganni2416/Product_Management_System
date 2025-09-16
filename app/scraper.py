# app/scraper.py

import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, Timeout, RequestException


def scrape_products(url: str, timeout: float = 5.0):
    """
    Scrape product details from the given URL.

    Args:
        url (str): The URL to scrape.
        timeout (float): Timeout in seconds for HTTP requests.

    Returns:
        list: List of dicts with product info (name, price, qty).
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.select(".thumbnail"):
            name = item.select_one(".title").get_text(strip=True)
            price_text = item.select_one(".price").get_text(strip=True)
            price = float(price_text.replace("$", ""))
            qty = 10  # default quantity as per original code
            products.append({"name": name, "price": price, "qty": qty})
        return products

    except HTTPError as http_err:
        print(f"HTTP error occurred during scraping: {http_err}")
    except Timeout as timeout_err:
        print(f"Timeout error occurred during scraping: {timeout_err}")
    except RequestException as req_err:
        print(f"Request exception occurred during scraping: {req_err}")
    # Removed catching bare Exception to avoid too general exception

    return []


if __name__ == "__main__":
    scrape_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
    print(f"Scraping from: {scrape_url}")
    data = scrape_products(scrape_url)
    print(f"Found {len(data)} products")

    # Send to API
    API_URL = "http://127.0.0.1:5000/api/products/"
    for p in data:
        res = requests.post(API_URL, json=p)
        print(f"→ {p['name']} | Status: {res.status_code}")
