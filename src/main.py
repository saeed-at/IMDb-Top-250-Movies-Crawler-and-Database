from utils.db import create_tables
import sys
from crawl import crawl_main_page_metadata, crawl_page
from config import BASE_URL
from models import Movie
from logger import setup_logging

crawl_logger = setup_logging('./crawling_logs.txt')


def crawl_main_page():
    """
    This method will call crawl_main_page_metadata and stores the results in a database with the create method.
    :return: None
    """
    links = crawl_main_page_metadata(BASE_URL)
    for link in links:
        # link = (rank, name, url, rating)
        Movie.create(rank=link[0], name=link[1], url=link[2], rating=link[3])


def crawl_movies():
    """
    This method will first get all movies in database that are not completed and then starts ex-taring information from
    each one's web page.
    :Return: None
    """
    movies = Movie.select().where(Movie.is_completed == 0)
    for movie in movies:
        information = crawl_page(movie.url)
        crawl_logger.info(f"|Started crawling ({movie.name}) movie({movie.rank} out of 250)...")
        movie.date = information['date']
        movie.description = information['description']
        movie.writers = information['stars']
        movie.stars = information['stars']
        movie.duration = information['duration']
        movie.category = information['category']
        movie.director = information['director']
        # set is_completed to 1, because crawling was successful.
        movie.is_completed = 1
        # save changes in a database
        movie.save()
    # print result for completed and non-completed movies available in database
    print(f"{Movie.select().where(Movie.is_completed==1).count()} movies has been crawled successfully, "
          f"{Movie.select().where(Movie.is_completed==0).count()} remained to crawl.")


def show_stats():
    """
    print result for completed and non-completed movies available in database
    :return: None
    """
    print(f"There are {Movie.select().where(Movie.is_completed==1).count()} completed records  and "
          f"{Movie.select().where(Movie.is_completed==0).count()} uncompleted records in the database.")


if __name__ == '__main__':
    if sys.argv[1] == 'create_tables':
        create_tables()
    elif sys.argv[1] == 'crawl_main_page':
        crawl_main_page()
    elif sys.argv[1] == 'crawl_movies':
        crawl_movies()
    elif sys.argv[1] == 'stats':
        show_stats()
