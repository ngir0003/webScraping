from movies import scrape_movies
from series import scrape_series
from db import init_db

if __name__ == "__main__":
    init_db()
    scrape_movies()
    scrape_series()