import requests
from bs4 import BeautifulSoup
import re
from config import BASE_URL

def get_page(url):
    """
    Takes an url of a page as input
    :return: the response of the request for the specific url
    """
    # You need to use headers for requesting, because without headers, imdb will find-out that you are scrapping, and it
    # will respond 403 error to you
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                      " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
    except:
        return None
    return response.text


def rank_name_extractor(content):
    """
     Search for rank and name in a div, characters before. Are related to the rank and characters after. Are related
     to the name of the movie
    :param content: <div> html code
    :return: rank[integer], name[string]
    """
    # search for this pattern [digit].[characters]
    pattern = r"(\d+)\.(.+)"
    match = re.match(pattern, content)
    # rank extraction
    before_dot = match.group(1)
    # name extraction
    after_dot = match.group(2)
    return int(before_dot), after_dot.lstrip(' ')


def crawl_main_page_metadata(base_url):
    """
    Crawl rating, rank and name of all movies from the main page and return them as a list.
    For each movie there is a set in metadata list: (rank, name, url, rating)
    :param base_url: The address for the main page
    :return: metadata list consists of url, rank, name and rating of each movie
    """
    # send request to the server
    response_text = get_page(base_url)

    soup = BeautifulSoup(response_text, 'html.parser')
    list_of_movies = soup.find_all('li',
                                   attrs={'class': 'ipc-metadata-list-summary-item sc-bca49391-0 eypSaE cli-parent'})
    metadata = []  # each element in this list consists of name, rank, url of relative movie
    for movie in list_of_movies:
        rank, name = rank_name_extractor(movie.find('h3', attrs={'class': 'ipc-title__text'}).text)
        rating = float(movie.find('span',
                                  attrs={'class': 'ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating'}).text[0:3])
        url = 'https://imdb.com' + movie.find('a', attrs={'class': 'ipc-title-link-wrapper'}).get('href')
        metadata.append((rank, name, url, rating))

    return metadata


def crawl_page(url):
    """
    This will crawl each page that is referred to a movie and extract all information like date, descriptions, director,
    writers, starts and ...
    :param url: Url which is related to a movie
    :return: metadata_information which consists all information above for a movies in a dictionary.
    """
    # send request to the site
    response = get_page(url)
    metadata_information = {}
    # check if the response has been received.
    if response != None:
        writers = []
        stars = []
        soup = BeautifulSoup(response, 'html.parser')
        # finding a list in html code that contains date, parent guide and duration of the movie
        date_pg_duration_list = soup.find('ul', attrs={
            'class': 'ipc-inline-list ipc-inline-list--show-dividers sc-afe43def-4 kdXikI baseAlt',
            'role': 'presentation'}).text

        metadata_information['date'] = date_pg_duration_list[0:4]

        duration_hour = re.findall(r'(\d{1} ?h)', date_pg_duration_list)
        duration_min = re.findall(r'(\d{1,2}m)', date_pg_duration_list)
        if not duration_min:
            duration = f"{int(duration_hour[0][:-1]) * 60}m"
        elif not duration_hour:
            duration = f"{int(duration_min[0][:-1])}m"
        else:
            duration = f"{int(duration_hour[0][:-1]) * 60 + int(duration_min[0][:-1])}m"
        metadata_information['duration'] = duration
        metadata_information['category'] = soup.find('div',
                                                     attrs={'class': 'ipc-chip-list__scroller'}).find('a').text

        metadata_information['description'] = soup.find('p', attrs={'class': 'sc-466bb6c-3 llCpwq'}).find('span',
                                                                                                          attrs={
                                                                                                              'class': 'sc-466bb6c-1 dRrIo'}).text
        # find div that contains director, writers and starts name of the movie
        dws_data = soup.find('div',
                             attrs={'class': 'sc-acac9414-3 hKIseD'}).find('div')  # dws stands director, writers, stars
        metadata_information['director'] = (
            dws_data.find('a', attrs={'class': 'ipc-metadata-list-item__list-content-item '
                                               'ipc-metadata-list-item__list-content-item--link'}).text)
        metadata = dws_data.find('ul', attrs={
            'class': 'ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt'})

        info = metadata.find_all('li')
        writer_index, stars_index = None, None
        for index, li in enumerate(info):
            # find the index for related li that shows the writers information
            if li.text.startswith('Writer'):
                writer_index = index
            # find the index for related li that shows the start information
            if li.text.startswith('Stars'):
                stars_index = index
        # extract writers names
        for writer in info[writer_index + 1:stars_index]:
            writers.append(writer.text)
        # extract starts name
        for star in info[stars_index + 1:]:
            stars.append(star.text)

        metadata_information['writers'] = writers
        metadata_information['stars'] = stars

        return metadata_information


if __name__ == '__main__':
    url = 'https://imdb.com/title/tt15398776/?ref_=chttp_t_80'
    print(f"This is crawl.py and for the test we are crawling {url}'s information...")
    res = crawl_page(url)
    for key in res.keys():
        print(key, ':', res[key])
