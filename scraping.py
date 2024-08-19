import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from file_and_data_utils import *


def website_scraping(website_url):
    """
    Goes over the home page of the website to scrape all the categories
    Creates the folder tree for data storage from the function folder_creation
    Stores the data of books from each category in a distinct CSV file from the function csv_writer

    :param website_url: url of the home page
    """
    # Get the HTML code of the page
    home_page = requests.get(website_url)
    # Parse the page HTML code
    soup = BeautifulSoup(home_page.content, 'html.parser')
    # Gets all the category lines
    nav_list = soup.find('ul', class_='nav-list').find('ul').find_all('a')

    # Gets all the categories URL and store them in a dictionary
    categories_dict = {}
    for line in nav_list:
        category_name = line.get_text(strip=True)
        category_relative_url = line.get('href')
        category_url = urljoin(website_url, category_relative_url)
        # Dictionary with category names as keys and categories urls as values
        categories_dict[category_name] = category_url

    # Creates a list containing all the categories names
    categories = categories_dict.keys()
    # Call the function folder_creation to create the folder tree for the storage
    main_storage_folder = folder_creation(categories)

    # Loops over all the category pages to get their content and creates a csv file per category
    for category_key in categories_dict:
        category_url = categories_dict[category_key]
        category_content = category_page_scraping(category_url, main_storage_folder)
        csv_writer(category_content, category_key, main_storage_folder)


def category_page_scraping(url_category, main_storage_folder):
    """
    Scrape a category page

    :param url_category: url of the category page
    :param main_storage_folder: folder in which the data needs to be stored .This function doesn't
    store any data itself but this parameter is necessary for the image download
    :return all_books_pages_content: List containing all the data for all the books scraped for
    this category
    """
    # Return variable : contain the information of all the books of a category
    all_books_pages_content = []

    # Get the HTML code of the category page
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
        next_page_relative_url = (category_soup.find('li', class_='next').find('a')
                                  .get('href'))
        next_page_url = urljoin(url_category, next_page_relative_url)
        # Recursive of the category_page_scraping function to go over all the pages of a category
        next_page_content = category_page_scraping(next_page_url, main_storage_folder)
        for line in next_page_content:
            all_books_pages_content.append(line)

    return all_books_pages_content


def product_page_scraping(page_url, main_storage_folder):
    """
    Scrape a specific product page of the website Books To Scrape.
    Calls the function image_download which download the cover of the book

    :param page_url: url of the page to scrape
    :param main_storage_folder: path to the folder where the data will be stored. Necessary for
    the image download
    :return: all the important data of product page
    """

    # Get the HTML content of the url and parse it with a Beautifulsoup html parser
    page = requests.get(page_url)
    product_soup = BeautifulSoup(page.content, 'html.parser')

    # Extraction of all the product properties

    # Get the name of the book
    title = product_soup.find('div', class_='col-sm-6 product_main').find('h1').get_text()

    # Get the description of the book
    # Initialized as 'no description available', modified if there is one
    product_description = "No description available for this book"
    if product_soup.find('div', id='product_description') is not None:
        product_description = (product_soup.find('div', id='product_description')
                               .find_next('p').get_text())
        product_description = txt_cleaning(product_description)

    # Scrape the table shown on the product page to extract the UPC, the price with and without
    # taxes and the number of books available
    product_table = product_soup.find('table', class_='table table-striped')
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
    # Same as for the prices, use of a re.search of a pattern to remove the '(' in front of
    # the number
    pattern = r'\((\d+)'
    match = re.search(pattern, availability_string)
    number_available = 0
    if match:
        number_available = int(match.group(1))

    # Scrape of the category
    category_list = product_soup.find(class_='breadcrumb').find_all('li')
    category = category_list[2].get_text(strip=True)

    # Scrape review rating
    rating_as_string = product_soup.find('p', class_="star-rating").get('class')
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
    image_relative_url = product_soup.find('img').get('src')
    # Clean the relative url
    image_relative_url = url_cleaning(image_relative_url)
    # Recreate the full url of the image
    base_url = "https://books.toscrape.com/"
    image_url = urljoin(base_url, image_relative_url)

    # Download the book's cover
    image_download(image_url, title, category, universal_product_code, main_storage_folder)

    return [title,
            product_description,
            category,
            universal_product_code,
            price_excluding_tax,
            price_including_tax,
            number_available,
            review_rating,
            image_url]
