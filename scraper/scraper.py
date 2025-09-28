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

    def get_books_urls(self) -> list[str]:
        '''This code snippet is part of a Python class that is used for web scraping book information
        from a website. Here's a breakdown of what the code is doing:'''

        books: List[ElementHandle] = self.page.query_selector_all("article.product_pod h3 a")
        books_urls: list[str] = [url_validator(urljoin(self.BASE_URL, book_url.get_attribute("href"))) if book_url else None for book_url in books] # todo Test and verify that validator works and the list contains valid URLs
        
        return books_urls
    
    def save_to_file(self, file):
        folder: str = "outputs"
        file_name: str = "book_data.json"
        file_path: Path = Path(folder, file_name)

        with open(file_path, "w", encoding = "utf-8") as f: # makes book_data.json file in the outputs folder 
                json.dump(file, f, indent = 2, ensure_ascii = False)
    
    def main_scraper(self) -> None:
        #TODO Add next page feature
        #TODO Test and validate the scraped Data
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless = False)
            self.page = self.browser.new_page()
            self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
            
            books_data: list[dict[str, Any]] = []    
            try:
                for book_url in self.get_books_urls():
                    # Visits every book page and scrapes relevant info
                    self.page.goto(book_url)

                    title: str = self.page.query_selector("div.product_main h1").inner_text()
                    description: str = self.page.query_selector(".product_page > p:nth-child(3)").inner_text()
                    price: str = self.page.query_selector("p.price_color").inner_text()
                    upc: str = self.page.query_selector("table.table-striped tr:first-child td").inner_text()
                    product_type: str = self.page.query_selector("table.table-striped tr:nth-child(2) td").inner_text()
                    price_without_tax: str = self.page.query_selector("table.table-striped tr:nth-child(3) td").inner_text()
                    pric_with_tax: str = self.page.query_selector("table.table-striped tr:nth-child(4) td").inner_text()
                    tax: str = self.page.query_selector("table.table-striped tr:nth-child(5) td").inner_text()
                    availability: str = self.page.query_selector("table.table-striped tr:nth-child(6) td").inner_text()
                    number_of_reviews: str = self.page.query_selector("table.table-striped tr:nth-child(7) td").inner_text()
                    star_rating: str = self.page.query_selector("p.star-rating").get_attribute("class").split()[-1]

                    book_data: dict[str, Any] = {
                        "title": title,
                        "description": description,
                        "price": price,
                        "upc": upc,
                        "product_type": product_type,
                        "price_without_tax": price_without_tax,
                        "price_with_tax": pric_with_tax,
                        "tax": tax,
                        "availability": availability,
                        "number_of_reviews": number_of_reviews,
                        "star_rating": star_rating
                    }

                    books_data.append(book_data)      
                
                self.save_to_file(books_data)

            except Exception as e:
                print(f"Error occurred: {e}")

if __name__ == "__main__":
    Browser().main_scraper()

#! next page cannot be scraped due to list of existing books not updating after changing the page.