# app/scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_products(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        products = []
        for item in soup.select(".thumbnail"):
            name = item.select_one(".title").get_text(strip=True)
            price = float(item.select_one(".price").get_text(strip=True).replace("$", ""))
            qty = 10
            products.append({"name": name, "price": price, "qty": qty})
        return products
    except Exception as e:
        print(f"Scraping failed: {e}")
        return []

if __name__ == "__main__":
    url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"
    print(f"Scraping from: {url}")
    data = scrape_products(url)
    print(f"Found {len(data)} products")

    # Send to API
    API_URL = "http://127.0.0.1:5000/api/products/"
    for p in data:
        res = requests.post(API_URL, json=p)
        print(f"→ {p['name']} | Status: {res.status_code}")
