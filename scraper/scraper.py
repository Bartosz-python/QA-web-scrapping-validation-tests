from playwright.sync_api import sync_playwright, Page, ElementHandle
from urllib.parse import urljoin
from typing import List, Any
from validator import url_validator
import json
from pathlib import Path

class Browser:
    def __init__(self):
        """The function initializes a Python class with a base URL for scraping book information."""

        self.BASE_URL = "https://books.toscrape.com/" #TODO TEST that the page is accessible
    
    def save_to_file(self, file):
        folder: str = "outputs"
        file_name: str = "book_data.json"
        file_path: Path = Path(folder, file_name)

        with open(file_path, "w", encoding = "utf-8") as f: # makes book_data.json file in the outputs folder 
            json.dump(file, f, indent = 2, ensure_ascii = False)
    
    def main_scraper(self) -> None:

        #TODO Test and validate the scraped Data

        #! Cookies and cups None description
        #! Add description back, as it was making an error

        with sync_playwright() as p:
            browser = p.chromium.launch(headless = False)
            page = browser.new_page()
            page.goto(self.BASE_URL, wait_until="domcontentloaded")
            
            books_data: list[dict[str, Any]] = []
            while True:

                current_page_url = page.url

                books = page.query_selector_all("article.product_pod h3 a")
                books_urls = [url_validator(urljoin(page.url, book_url.get_attribute("href"))) if book_url else None for book_url in books]

                for book_url in books_urls:
                    # Visits every book page and scrapes relevant info
                    page.goto(book_url, wait_until = "domcontentloaded")

                    title: str = page.query_selector("div.product_main h1").inner_text()
                    price: str = page.query_selector("p.price_color").inner_text()
                    upc: str = page.query_selector("table.table-striped tr:first-child td").inner_text()
                    product_type: str = page.query_selector("table.table-striped tr:nth-child(2) td").inner_text()
                    price_without_tax: str = page.query_selector("table.table-striped tr:nth-child(3) td").inner_text()
                    pric_with_tax: str = page.query_selector("table.table-striped tr:nth-child(4) td").inner_text()
                    tax: str = page.query_selector("table.table-striped tr:nth-child(5) td").inner_text()
                    availability: str = page.query_selector("table.table-striped tr:nth-child(6) td").inner_text()
                    number_of_reviews: str = page.query_selector("table.table-striped tr:nth-child(7) td").inner_text()
                    star_rating: str = page.query_selector("p.star-rating").get_attribute("class").split()[-1]
                    url = book_url

                    book_data: dict[str, Any] = {
                        "title": title,
                        "price": price,
                        "upc": upc,
                        "product_type": product_type,
                        "price_without_tax": price_without_tax,
                        "price_with_tax": pric_with_tax,
                        "tax": tax,
                        "availability": availability,
                        "number_of_reviews": number_of_reviews,
                        "star_rating": star_rating,
                        "book_url": url
                    }

                    books_data.append(book_data)

                page.goto(current_page_url, wait_until = "domcontentloaded")
                next_page_btn = page.query_selector("li.next a")

                if not next_page_btn:
                    break

                next_page_url = next_page_btn.get_attribute("href")
                full_next_page_url = url_validator(urljoin(current_page_url, next_page_url))

                page.goto(full_next_page_url, wait_until = "domcontentloaded")

            self.save_to_file(books_data)

if __name__ == "__main__":
    Browser().main_scraper()