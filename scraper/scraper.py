from playwright.sync_api import sync_playwright, Page
from urllib.parse import urljoin
from typing import Any
from validator import url_validator
import json
from pathlib import Path

class Book:
    """Book structure class"""
    def __init__(self, title, price, upc, product_type, price_without_tax, price_with_tax,
                tax,
                availability,
                number_of_reviews,
                star_rating,
                url
        ):
        
        self.title: str = title
        self.price: str = price
        self.upc: str = upc
        self.product_type: str = product_type
        self.price_without_tax: str = price_without_tax
        self.price_with_tax: str = price_with_tax
        self.tax: str = tax
        self.availability: str = availability
        self.number_of_reviews: str = number_of_reviews
        self.star_rating: str = star_rating
        self.url: str = url

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
    
class Scraper:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def get_books_urls(self) -> list[str]:
        """Get all book URLs from current page."""
        books = self.page.query_selector_all("article.product_pod h3 a")
        return [url_validator(urljoin(self.page.url, book_url.get_attribute("href"))) for book_url in books if book_url]

    def scrape_book_data(self, url: str) -> Book:
        '''The code snippet you provided is defining a method within the `Scraper` class called
        `scrape_book_data`. This method is responsible for scraping data from a specific book page
        given its URL.'''

        self.page.goto(url, wait_until = "domcontentloaded")

        title: str = self.page.query_selector("div.product_main h1").inner_text()
        price: str = self.page.query_selector("p.price_color").inner_text()
        upc: str = self.page.query_selector("table.table-striped tr:first-child td").inner_text()
        product_type: str = self.page.query_selector("table.table-striped tr:nth-child(2) td").inner_text()
        price_without_tax: str = self.page.query_selector("table.table-striped tr:nth-child(3) td").inner_text()
        price_with_tax: str = self.page.query_selector("table.table-striped tr:nth-child(4) td").inner_text()
        tax: str = self.page.query_selector("table.table-striped tr:nth-child(5) td").inner_text()
        availability: str = self.page.query_selector("table.table-striped tr:nth-child(6) td").inner_text()
        number_of_reviews: str = self.page.query_selector("table.table-striped tr:nth-child(7) td").inner_text()
        star_rating: str = self.page.query_selector("p.star-rating").get_attribute("class").split()[-1]

        return Book(title, price, upc, product_type, price_without_tax, price_with_tax, tax, availability, number_of_reviews, star_rating, url)
    
    def get_next_page_url(self):
        next_page_btn = self.page.query_selector("li.next a")
        if not next_page_btn:
            return False
        
        return url_validator(urljoin(self.page.url, next_page_btn.get_attribute("href")))

class Browser:
    def __init__(self, base_url = "https://books.toscrape.com/"):

        self.BASE_URL = base_url
    
    def save_to_file(self, books: list[Book], file_name: str) -> None:
        folder: str = "outputs"
        file_path: Path = Path(folder, file_name)

        with open(file_path, "w", encoding = "utf-8") as f: # makes book_data.json file in the outputs folder 
            json.dump([book.to_dict() for book in books if book], f, indent = 2, ensure_ascii = False)

    def run(self) -> None:
        '''Main method that runs the script.'''
        #! Add description back, as it was making an error with overflown text

        books_data: list[Book] = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless = False)
            page = browser.new_page()
            page.goto(self.BASE_URL, wait_until="domcontentloaded")
            
            scraper = Scraper(page, page.url)

            while True:
                current_page_url = page.url
                try:

                    books_urls = scraper.get_books_urls()

                    for book_url in books_urls: # Visits every book page and scrapes relevant info
                        book = scraper.scrape_book_data(book_url)
                        books_data.append(book)

                    page.goto(current_page_url, wait_until= "domcontentloaded")
                    next_page = scraper.get_next_page_url()
                    page.goto(next_page, wait_until = "domcontentloaded")

                except Exception as e:
                    print(f"error: {e}")
                    break

            self.save_to_file(books_data, "book_data.json")

if __name__ == "__main__":
    Browser().run()