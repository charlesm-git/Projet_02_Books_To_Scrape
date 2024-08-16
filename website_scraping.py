import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from category_scraping import category_page_scraping, csv_writer
import os
import datetime
import shutil


def website_scraping(website_url):
    # Get the HTML code of the page
    home_page = requests.get(website_url)
    # Parse the page HTML code
    soup = BeautifulSoup(home_page.content, 'html.parser')

    nav_list = soup.find('ul', class_='nav-list').find('ul').find_all('a')

    categories_dict = {}

    for line in nav_list:
        category_name = line.get_text(strip=True)
        category_relative_url = line.get('href')
        category_url = urljoin(website_url, category_relative_url)
        categories_dict[category_name] = category_url

    # Get the date od the extract
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    # Path of the storage folder
    storage_folder = f'./data_{timestamp}'
    # If the folder already exists, the program deletes it
    if os.path.exists(storage_folder):
        shutil.rmtree(storage_folder)
    # Creates the new storage folder
    os.mkdir(storage_folder)

    for category_key in categories_dict:
        category_url = categories_dict[category_key]
        category_content = category_page_scraping(category_url)
        csv_writer(category_content, category_key, storage_folder)

if __name__ == "__main__":
    # URL to scrape
    website = "https://books.toscrape.com"
    website_scraping(website)

    # url_test = "https://books.toscrape.com/catalogue/category/books/classics_6/index.html"
    # category_content_test = category_page_scraping(url_test)
    # csv_writer(category_content_test, 'TEST', './')
