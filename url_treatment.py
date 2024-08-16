def url_cleaning(url_to_clean):
    """
    Function used to clean relative URL by removing '../../..' segments

    :param url_to_clean: URL that needs to be cleaned in order to be joined
    :return url_cleaned: URL where all the '../../' have been removed
    """
    parts = url_to_clean.split('/')
    cleaned_parts = []

    # Remove segments with '..' and '.'
    for part in parts:
        if part not in ['..', '.', '']:
            cleaned_parts.append(part)

    url_cleaned = '/'.join(cleaned_parts)

    return url_cleaned
