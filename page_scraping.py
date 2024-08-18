import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
from url_treatment import url_cleaning


def txt_cleaning(text):
    # List of all the forbidden characters in a file name
    forbidden_characters = r'[\/:*?"<>|,;.`]'
    # Use of the re.sub to remove all the forbidden characters and replace them by '_'
    cleaned_text = re.sub(forbidden_characters, '', text)
    cleaned_text = cleaned_text.replace("'", "")
    return cleaned_text


def txt_shortening(text):
    max_length = 150
    # If the length of the name exceed 150 characters, shorten it to 150
    if len(text) > max_length:
        text = text[:max_length]
    return text


def image_download(image_url, image_name, image_category, main_storage_folder):
    image = requests.get(image_url)
    image_name = txt_cleaning(image_name)
    image_name = txt_shortening(image_name)
    image_name = image_name.replace(' ', '_')
    image_category = image_category.replace(' ', '_')
    with open(f'{main_storage_folder}/images/{image_category}/{image_name}.jpg', 'wb') as image_file:
        image_file.write(image.content)


def product_page_scraping(page_url, main_storage_folder):
    """
    Scrape a specific page of the website Books To Scrape.
    Calls the function image_download which download the cover of the book

    :param page_url: url of the page to scrape
    :param main_storage_folder: path to the folder where the data will be stored. Necessary for
    the image download
    :return: all the interesting parameter of product page
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
        product_description = txt_cleaning(product_description)

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

    # Scrape image url
    # Get the relative url first
    image_relative_url = soup.find('img').get('src')
    # Clean the relative url
    image_relative_url = url_cleaning(image_relative_url)
    # Recreate the full url of the image
    base_url = "https://books.toscrape.com/"
    image_url = urljoin(base_url, image_relative_url)

    # Download the book's cover
    image_download(image_url, title, category, main_storage_folder)

    return [title,
            product_description,
            category,
            universal_product_code,
            price_excluding_tax,
            price_including_tax,
            number_available,
            review_rating,
            image_url]
