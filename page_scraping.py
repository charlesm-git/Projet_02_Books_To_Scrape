import requests
from bs4 import BeautifulSoup
import re
import csv


def product_page_scraping(page_url):
    """
    Scrape a specific page of the website Books To Scrape

    :param page_url: URL of the page to scrape
    :return: list of all the useful information
    """

    # Get the HTML content of the url and parse it with a Beautifulsoup html parser
    page = requests.get(page_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Extraction of all the product properties

    # Get the name of the book
    title = soup.find('div', class_='col-sm-6 product_main').find('h1').get_text()

    # Get the description of the book
    # Initialized as 'no description available', modified if there is one
    product_description = "No description available for this book"
    if soup.find('div', id='product_description') is not None:
        product_description = soup.find('div', id='product_description').find_next('p').get_text()

    # Scrape the table shown on the product page to extract the UPC, the price with and without taxes
    # and the number of books available
    product_table = soup.find('table', class_='table table-striped')
    table_content = product_table.find_all('td')

    # Scraping UPC
    universal_product_code = table_content[0].get_text()

    # Scraping prices (both with and without taxes)
    price_excluding_tax = table_content[2].get_text()
    price_including_tax = table_content[3].get_text()
    # Use of re.search of a pattern to remove the £ symbol from the prices
    pattern = r'£(\d+.\d+)'
    match = re.search(pattern, price_excluding_tax)
    price_excluding_tax = float(match.group(1))
    match = re.search(pattern, price_including_tax)
    price_including_tax = float(match.group(1))

    # Number of books available extracted from the string
    availability_string = table_content[5].get_text()
    # Same as for the prices, use of a re.search of a pattern to remove the '(' in front of the number
    pattern = r'\((\d+)'
    match = re.search(pattern, availability_string)
    number_available = 0

    if match:
        number_available = int(match.group(1))

    # Scrape of the category
    category_list = soup.find(class_='breadcrumb').find_all('li')
    category = category_list[2].get_text(strip=True)

    # Scrape image url
    image_url = soup.find('img').get('src')

    # Scrape review rating
    rating_as_string = soup.find('p', class_="star-rating").get('class')
    rating_as_word = rating_as_string[1]

    match rating_as_word:
        case "One":
            review_rating = 1
        case "Two":
            review_rating = 2
        case "Three":
            review_rating = 3
        case "Four":
            review_rating = 4
        case "Five":
            review_rating = 5
        case _:
            review_rating = 0

    return [title,
            product_description,
            category,
            universal_product_code,
            price_excluding_tax,
            price_including_tax,
            number_available,
            review_rating,
            image_url]
