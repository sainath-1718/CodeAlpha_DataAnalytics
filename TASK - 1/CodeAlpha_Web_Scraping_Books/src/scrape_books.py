"""
CodeAlpha Data Analytics Internship — Task 1: Web Scraping
Project: Books and Prices
Source: https://books.toscrape.com/ (practice website)

Usage:
    pip install -r requirements.txt
    python src/scrape_books.py --pages 2

This script fetches pages from the practice site and saves extracted records to CSV.
It also prints a small data-quality summary. It does not bypass access controls.
"""
import argparse
import logging
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

BASE_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "books_dataset.csv"
HEADERS = {"User-Agent": "CodeAlpha-WebScraping-StudentProject/1.0 (educational use)"}
REQUEST_TIMEOUT = 20
REQUEST_DELAY_SECONDS = 1.0
MAX_PAGES_DEFAULT = 2

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_rating(class_list):
    """Convert a star-rating CSS class to an integer 1–5, or None."""
    mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    for item in class_list or []:
        if item in mapping:
            return mapping[item]
    return None


def scrape_page(session, page_url):
    """Fetch one catalogue page and return a list of book dictionaries."""
    response = session.get(page_url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    records = []

    for card in soup.select("article.product_pod"):
        title_link = card.select_one("h3 a")
        price_node = card.select_one(".price_color")
        rating_node = card.select_one(".star-rating")
        availability_node = card.select_one(".availability")

        if title_link is None or price_node is None:
            logging.warning("Skipping a card because title or price was missing.")
            continue

        title = title_link.get("title", title_link.get_text(strip=True))
        relative_url = title_link.get("href", "")
        product_url = urljoin(page_url, relative_url)

        # Site displays GBP prices. Remove non-numeric characters safely.
        raw_price = price_node.get_text(strip=True)
        numeric_price = re.sub(r"[^0-9.]", "", raw_price)
        price = float(numeric_price) if numeric_price else None

        availability = (
            availability_node.get_text(" ", strip=True)
            if availability_node is not None
            else "Unknown"
        )

        records.append({
            "Book_Name": title,
            "Price_GBP": price,
            "Rating_Stars": parse_rating(
                rating_node.get("class", []) if rating_node else []
            ),
            "Availability": availability,
            "Product_URL": product_url,
        })

    return records


def main():
    parser = argparse.ArgumentParser(description="Scrape book titles and prices.")
    parser.add_argument(
        "--pages", type=int, default=MAX_PAGES_DEFAULT,
        help="Number of catalogue pages to scrape (default: 2; maximum: 50)."
    )
    parser.add_argument("--output", default=str(OUTPUT_FILE), help="Output CSV path.")
    args = parser.parse_args()

    if args.pages < 1 or args.pages > 50:
        parser.error("--pages must be between 1 and 50.")

    all_records = []
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with requests.Session() as session:
        session.headers.update(HEADERS)
        for page_number in range(1, args.pages + 1):
            page_url = BASE_URL if page_number == 1 else urljoin(
                BASE_URL, f"catalogue/page-{page_number}.html"
            )
            logging.info("Scraping page %s: %s", page_number, page_url)
            try:
                records = scrape_page(session, page_url)
                if not records:
                    logging.warning("No books found on page %s; stopping.", page_number)
                    break
                all_records.extend(records)
            except RequestException as exc:
                logging.error("Could not retrieve page %s: %s", page_number, exc)
                break
            time.sleep(REQUEST_DELAY_SECONDS)

    if not all_records:
        logging.error(
            "No live records were collected. Check internet access and the source website. "
            "A sample dataset is available at data/books_dataset_sample.csv."
        )
        raise SystemExit(1)

    result = pd.DataFrame(all_records)
    result = result.drop_duplicates(subset=["Product_URL"])
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False, encoding="utf-8")

    print("\n--- SCRAPING SUMMARY ---")
    print(f"Records saved: {len(result)}")
    print(f"Columns: {', '.join(result.columns)}")
    print(f"Missing values per column:\n{result.isna().sum().to_string()}")
    print(f"Duplicate product URLs: {result['Product_URL'].duplicated().sum()}")
    print(f"Output file: {output_path}")
    if result["Price_GBP"].notna().any():
        print(f"Minimum price (£): {result['Price_GBP'].min():.2f}")
        print(f"Maximum price (£): {result['Price_GBP'].max():.2f}")
        print(f"Average price (£): {result['Price_GBP'].mean():.2f}")


if __name__ == "__main__":
    main()
