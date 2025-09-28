from playwright.sync_api import sync_playwright, Page, ElementHandle
from urllib.parse import urljoin
from typing import List, Any
from validator import url_validator
import json
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
        folder = "outputs/" # add / in the end to indicate the file in the folder 
        filename = "book_data.json"

        filepath = f"{folder}{filename}"
        with open(filepath, "w") as f: # makes book_data.json file in the outputs folder 
                json.dump(file, f, indent = 2, ensure_ascii = False)
    
    def main_scraper(self) -> None:
        #TODO Add rest of the items to scrape
        #TODO Add next page feature
        #TODO Test and validate the scraped Data
        #TODO Write the scraped data to .json file which will be transormed to .xslx
        with sync_playwright() as p:
            self.browser: Browser = p.chromium.launch(headless = False)
            self.page: Page = self.browser.new_page()
            self.page.goto(self.BASE_URL, wait_until="domcontentloaded")
            
            books_data: list[dict[str, Any]] = [] 
            try:
                for book_url in self.get_books_urls():
                    # Visits every book page and scrapes relevant info
                    self.page.goto(book_url)

                    title: str = self.page.query_selector("div.product_main h1").inner_text()
                    description: str = 1
                    price: str = 2
                    upc: str = 3
                    product_type: str = 4
                    price_without_tax: str = 5
                    pric_with_tax: str = 6
                    tax: str = 7
                    availability: str = 8
                    number_of_reviews: str = 9
                    star_rating: str = 10
        
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