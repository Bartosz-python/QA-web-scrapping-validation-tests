from playwright.sync_api import sync_playwright, Page, ElementHandle
from urllib.parse import urljoin
from typing import List, Optional
class Browser:
    def __init__(self):
        """The function initializes a Python class with a base URL for scraping book information."""

        self.BASE_URL = "https://books.toscrape.com/" #TODO TEST that the page is accessible

    def get_book_urls(self) -> list[str]:
        # This code snippet is part of a Python class that is used for web scraping book information
        # from a website. Here's a breakdown of what the code is doing:

        books: List[ElementHandle] = self.page.query_selector_all("article.product_pod h3 a")
        books_url: list[str] = [urljoin(self.BASE_URL, book_url.get_attribute("href")) if book_url else None for book_url in books] #TODO Add valid URL validator || Test and verify that validator works and the list contains valid URLs
        
        return books_url
    
    def main_scraper(self) -> None:
        #TODO Add rest of the items to scrape
        #TODO Add next page feature
        #TODO Test and validate the scraped Data
        with sync_playwright() as p:
            self.browser = p.chromium.launch(headless = False)
            self.page: Page = self.browser.new_page()
            self.page.goto(self.BASE_URL, wait_until="domcontentloaded")

            try:
                for book_url in self.get_book_urls():
                    self.page.goto(book_url) # 1. Visits a book page. 
                    title = self.page.query_selector("div.product_main h1").inner_text() # 2. Scrapes the header title.
                    print(title)
            except Exception as e:
                print(f"Error occurred: {e}")

if __name__ == "__main__":
    Browser().main_scraper()