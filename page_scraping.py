import requests
from bs4 import BeautifulSoup
import re

# url to scrape
url = "https://books.toscrape.com/catalogue/the-long-haul-diary-of-a-wimpy-kid-9_757/index.html"

# Get the HTML content of the url and parse it with a Beautifulsoup html parser
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')


# Extraction of all the product properties

# Get the product page url
# TO BE DONE

# Get the name of the book
title = soup.find('div', class_='col-sm-6 product_main').find('h1').get_text()

# Get the description of the book
product_description = soup.find('div', id='product_description').find_next('p').get_text()

# Scrape the table shown on the product page to extract the UPC, the price with and without taxes
# and the number of books available

product_table = soup.find('table', class_='table table-striped')
table_content = product_table.find_all('td')

# UPC, price with and without taxes taken directly from the table scraping
universal_product_code = table_content[0].get_text()
price_excluding_tax = table_content[2].get_text()
price_including_tax = table_content[3].get_text()

# Number of books available extracted from the string
availability_string = table_content[5].get_text()
pattern = r'\((\d+)'
match = re.search(pattern, availability_string)
number_available = 0

if match:
    number_available = match.group(1)

# Scrape of the category

category_list = soup.find(class_='breadcrumb').find_all('li')
category = category_list[2].get_text(strip=True)

# Scrape image url

image_url = soup.find('img').get('src')

print(title)
print(product_description)
print(universal_product_code)
print(price_excluding_tax)
print(price_including_tax)
print(number_available)
print(category)
print(image_url)
