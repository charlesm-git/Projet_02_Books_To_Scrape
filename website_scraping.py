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

    # Gets all the categories URL and store them in a dictionary
    categories_dict = {}
    for line in nav_list:
        category_name = line.get_text(strip=True)
        category_relative_url = line.get('href')
        category_url = urljoin(website_url, category_relative_url)
        categories_dict[category_name] = category_url

    categories = categories_dict.keys()
    main_storage_folder = folder_creation(categories)

    for category_key in categories_dict:
        category_url = categories_dict[category_key]
        category_content = category_page_scraping(category_url, main_storage_folder)
        csv_writer(category_content, category_key, main_storage_folder)


def folder_creation(category_names):
    # Get the date of the extract
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    # Path of the storage folder
    main_storage_folder = f'./data_{timestamp}'
    image_folder = f'{main_storage_folder}/images'
    # If the folder already exists, the program deletes it
    if os.path.exists(main_storage_folder):
        shutil.rmtree(main_storage_folder)
    # Creates the new storage folder
    os.mkdir(main_storage_folder)
    os.mkdir(image_folder)

    for name in category_names:
        name = name.replace(' ', '_')
        os.mkdir(f'{image_folder}/{name}')

    return main_storage_folder


if __name__ == "__main__":
    # URL to scrape
    website = "https://books.toscrape.com"
    website_scraping(website)

    # url_test = "https://books.toscrape.com/catalogue/category/books/classics_6/index.html"
    # category_content_test = category_page_scraping(url_test)
    # csv_writer(category_content_test, 'TEST', './')

    # url_test = "https://books.toscrape.com/catalogue/emma_17/index.html"
    # page_content_test = product_page_scraping(url_test)
    # csv_writer(page_content_test, 'TEST', './')
    # image_download(page_content_test[8], page_content_test[0], page_content_test[2], 'image')
