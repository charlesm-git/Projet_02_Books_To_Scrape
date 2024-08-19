import os
import datetime
import shutil
import re
import requests
import csv


def txt_cleaning(text):
    """
    Remove all unwanted characters in a text to make the saving more reliable

    :param text: text that needs to be cleaned
    :return: text where all the unwanted characters have been removed
    """
    # List of all the unwanted characters
    forbidden_characters = r'[\/:*?"<>|,;.`]'
    # Use of the re.sub to remove all the forbidden characters
    cleaned_text = re.sub(forbidden_characters, '', text)
    # Apostrophes are removed on their own
    cleaned_text = cleaned_text.replace("'", "")
    cleaned_text = cleaned_text.replace('"', '')
    return cleaned_text


def txt_shortening(text):
    """
    Shorten a text to 130 characters if its length is longer

    :param text: text that could need to be shortened
    :return: text shortened
    """
    max_length = 130
    # If the length of the text exceed 150 characters, shorten it to 150
    if len(text) > max_length:
        text = text[:max_length]
    return text


def url_cleaning(url_to_clean):
    """
    Function used to clean relative URL by removing '../../..' segments

    :param url_to_clean: URL that needs to be cleaned in order to be joined
    :return url_cleaned: URL where all the '../../' have been removed
    """
    # Decompose the url into parts
    parts = url_to_clean.split('/')
    cleaned_parts = []
    # Remove segments with '..' and '.'
    for part in parts:
        if part not in ['..', '.', '']:
            cleaned_parts.append(part)
    # rejoin all the parts with '/' separating them
    url_cleaned = '/'.join(cleaned_parts)

    return url_cleaned


def folder_creation(category_names):
    """
    Creates the folder tree for the storage of all the data collected.
    The main folder will be named after the date at which the data is extracted.

    :param category_names: name of the books categories. Used to create the folder tree
    :return main_storage_folder: Name of the main storing folder
    """

    # Get the date of the extract
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    # Path of the storage folder
    main_storage_folder = f'./data_{timestamp}'
    image_folder = f'{main_storage_folder}/images'
    # If the folder already exists, the program deletes it
    if os.path.exists(main_storage_folder):
        shutil.rmtree(main_storage_folder)
    # Creates the new storage folders : the main and the image folder, containing itself one folder
    # for each book category
    os.mkdir(main_storage_folder)
    os.mkdir(f'{main_storage_folder}/CSV')
    os.mkdir(image_folder)
    for name in category_names:
        name = name.replace(' ', '_')
        os.mkdir(f'{image_folder}/{name}')

    return main_storage_folder


def image_download(image_url, image_name, image_category, image_upc, main_storage_folder):
    """
    Create and store in the right folder the file of a given image (url)

    :param image_url: url of the image to download
    :param image_name: name wanted for the image
    :param image_category: category of the book, Necessary to store the image in the right folder
    :param main_storage_folder: name of the main storage folder 'data_...'
    """
    # Get the content of the url provided
    image = requests.get(image_url)
    # Cleans the name and category provided to make sure that it suits all requirements (forbidden
    # characters, no space, etc.)
    image_name = txt_cleaning(image_name)
    image_name = txt_shortening(image_name)
    image_name = image_name.replace(' ', '_')
    image_category = image_category.replace(' ', '_')
    # Creation of the file and download of the image in the right folder
    with (open(f'{main_storage_folder}/images/{image_category}/{image_name}_{image_upc}.jpg', 'wb') as
          image_file):
        image_file.write(image.content)


def csv_writer(csv_content, category_name, main_storage_folder):
    """
    Creates the csv file and store all the data for a given book category

    :param csv_content: data to store
    :param category_name: name of the category books category treated
    :param main_storage_folder: Folder in which the csv file will be saved
    """
    # Definition of the header
    header = ["product_page_url", "title", "product_description", "category", "UPC",
              "price_excluding_tax", "price_including_tax", "number_available", "review_rating",
              "image_url"]
    # Creation and writing of the csv file in the right folder
    with (open(f'{main_storage_folder}/CSV/{category_name}.csv', 'w', encoding='utf-8', newline='')
          as csv_file):
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(header)
        writer.writerows(csv_content)
