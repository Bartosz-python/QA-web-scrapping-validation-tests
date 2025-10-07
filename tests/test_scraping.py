"""In this file there will be main logic of the unittests that will validate the scraper/scraper.py code in context of proper data fetching and logic"""
import pytest
from src.scraper import Scraper
import requests
from playwright.sync_api import sync_playwright

@pytest.mark.smoke
def test_url():
    response = requests.get("https://books.toscrape.com/")
    assert response.status_code == 200

@pytest.mark.validation
def test_get_books_urls():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("https://books.toscrape.com/", wait_until = "domcontentloaded")
        
        scrap_test = Scraper(page, page.url)
        books_test = scrap_test.get_books_urls()

    assert books_test[0] == "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

@pytest.mark.validation
def test_scrape_book_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("https://books.toscrape.com/", wait_until = "domcontentloaded")
        scrap_test = Scraper(page, page.url)
        books = scrap_test.get_books_urls()
        
        book_data = scrap_test.scrape_book_data(books[0])
        
    assert book_data.title == "A Light in the Attic"
    assert book_data.star_rating == 3

@pytest.mark.validation
def test_get_next_page_url_different_url_no_page_button():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("https://example.com", wait_until = "domcontentloaded")
        scrap_test = Scraper(page, page.url)
        next_page_test = scrap_test.get_next_page_url()

        assert next_page_test == None

@pytest.mark.validation
def test_get_next_page_url_valid():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = True)
        page = browser.new_page()
        page.goto("https://books.toscrape.com/", wait_until = "domcontentloaded")
        scrap_test = Scraper(page, page.url)
        next_page_test = scrap_test.get_next_page_url()

        assert next_page_test == "https://books.toscrape.com/catalogue/page-2.html"