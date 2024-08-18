import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from page_scraping import product_page_scraping
from url_treatment import url_cleaning
import csv


def csv_writer(csv_content, category_name, main_storage_folder):

    # put everything in a csv file
    header = ["product_page_url", "title", "product_description", "category", "UPC", "price_excluding_tax",
              "price_including_tax", "number_available", "review_rating", "image_url"]

    with open(f'{main_storage_folder}/{category_name}.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)
        writer.writerows(csv_content)


def category_page_scraping(url_category, main_storage_folder):
    # Return variable : contain the information of all the books of a category
    all_books_pages_content = []

    # Get the HTML code of the page
    category_page = requests.get(url_category)
    # Parse the page HTML code
    category_soup = BeautifulSoup(category_page.content, 'html.parser')

    # Get all the Books items to then extract their url
    books = category_soup.find_all('div', class_='image_container')

    # Base URL used to reformat the book pages scraped URL
    base_url = "https://books.toscrape.com/catalogue/"

    # List of all the URL of this category reformated
    books_url_list = []

    # Creation of a list containing all the books pages URL of this page
    for book in books:
        # Get the relative URL of the book page
        book_relative_url = book.find('a').get('href')
        # Clean the URL with the function url_cleaning
        book_relative_url = url_cleaning(book_relative_url)
        # Join base and relative URL
        book_url = urljoin(base_url, book_relative_url)
        # Add to the main list containing all the URLs
        books_url_list.append(book_url)

    # Loops over all the url to get the content of each book pages
    for book_url in books_url_list:
        # Call of the page_scraping function
        page_content = product_page_scraping(book_url, main_storage_folder)
        # Adding the url of the page to the results in first position
        page_content.insert(0, book_url)
        print(page_content)
        # Add the results of the page scraping to a common list
        all_books_pages_content.append(page_content)

    # Check if there is another page (presence of a 'next' button)
    pager_check = category_soup.find('li', class_='next') is not None
    # If there is a 'next' button, call of the category_page_scraping function itself to scrap
    # the next page
    if pager_check:
        next_page_relative_url = category_soup.find('li', class_='next').find('a').get('href')
        next_page_url = urljoin(url_category, next_page_relative_url)
        # Recursive of the category_page_scraping function to go over all the pages of a category
        next_page_content = category_page_scraping(next_page_url, main_storage_folder)
        for line in next_page_content:
            all_books_pages_content.append(line)

    return all_books_pages_content
