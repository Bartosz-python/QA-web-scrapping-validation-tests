from playwright.sync_api import sync_playwright, Page
from urllib.parse import urljoin
from typing import Any
from validator import url_validator, is_proper_type, is_existing, convert_to_int_if_in_hashmap
import json
from excel_writer import save_json_to_excel

class Book:
    """Book structure class"""
    def __init__(self, title, description, price, upc, product_type, price_without_tax, price_with_tax,
                tax,
                availability,
                number_of_reviews,
                star_rating,
                url
        ):
        
        self.title = title
        self.description = description
        self.price = price
        self.upc = upc
        self.product_type = product_type
        self.price_without_tax = price_without_tax
        self.price_with_tax = price_with_tax
        self.tax = tax
        self.availability = availability
        self.number_of_reviews = number_of_reviews
        self.star_rating = star_rating
        self.url = url

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
    
class Scraper:
    """Responsible for the scraping feature by getting all the neccessary URLs, scrapping all the data and moving into next page"""
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url

    def get_books_urls(self) -> list[str]:
        """Get all book URLs from current page."""
        books = self.page.query_selector_all("article.product_pod h3 a")
        return [url_validator(urljoin(self.page.url, book_url.get_attribute("href"))) for book_url in books if book_url]

    def scrape_book_data(self, book_url: str) -> Book:
        """This method is responsible for scraping data from a specific book page
        given its URL."""
        if url_validator(book_url):

            self.page.goto(book_url, wait_until = "domcontentloaded")

            title: str = is_proper_type(is_existing(self.page.query_selector("div.product_main h1")), str)
            description: str = is_proper_type(is_existing(self.page.query_selector("div#product_description + p")), str)
            price: str = is_proper_type(is_existing(self.page.query_selector("p.price_color")), str)
            upc: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:first-child td")), str)
            product_type: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:nth-child(2) td")), str)
            price_without_tax: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:nth-child(3) td")), str)
            price_with_tax: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:nth-child(4) td")), str)
            tax: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:nth-child(5) td")), str)
            availability: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:nth-child(6) td")), str)
            number_of_reviews: str = is_proper_type(is_existing(self.page.query_selector("table.table-striped tr:nth-child(7) td")), str)

            star_map: dict[str, int] = {
                "One" : 1,
                "Two" : 2,
                "Three": 3,
                "Four" : 4,
                "Five" : 5
            }
            
            star_rating_element: str = self.page.query_selector("p.star-rating")
            if not star_rating_element:
                star_rating = "No star rating for this book"

            star_rating = convert_to_int_if_in_hashmap(is_proper_type(star_rating_element.get_attribute("class").split()[-1], str), star_map)
                
            return Book(title, description, price, upc, product_type, price_without_tax, price_with_tax, tax, availability, number_of_reviews, star_rating, book_url)
        raise Exception("Given URL is invalid")
    
    def get_next_page_url(self) -> str:
        next_page_btn = self.page.query_selector("li.next a")
        if not next_page_btn:
            print(f"No button available")
            return
        return url_validator(urljoin(self.page.url, next_page_btn.get_attribute("href")))
    
class Browser:
    def __init__(self, base_url: str = "https://books.toscrape.com/"):

        self.BASE_URL = base_url #TODO Check if it is accessible <-

    def run(self) -> None:
        """Main method that runs the script."""

        books_data: list[Book] = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless = False)
            page = browser.new_page()
            page.goto(self.BASE_URL, wait_until="domcontentloaded")
            
            scraper = Scraper(page, page.url)

            while True:
                current_page_url: str = page.url
                try:
                    books_urls: list[str] = scraper.get_books_urls()

                    for book_url in books_urls:
                        book = scraper.scrape_book_data(book_url)
                        books_data.append(book)

                    page.goto(current_page_url, wait_until= "domcontentloaded")
                    next_page = scraper.get_next_page_url()
                    page.goto(next_page, wait_until = "domcontentloaded")

                except Exception as e:
                    print(f"error: {e}")
                    break

            self.save_to_json(books_data)

        save_json_to_excel()

    def save_to_json(self, books: list[Book], file_path: str = "outputs/book_data.json") -> None:
        with open(file_path, "w", encoding = "utf-8") as f: # makes book_data.json file in the outputs folder 
            json.dump([book.to_dict() for book in books if book], f, indent = 2, ensure_ascii = False)
    
if __name__ == "__main__":
    Browser().run()