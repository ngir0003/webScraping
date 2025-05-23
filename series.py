import requests
from bs4 import BeautifulSoup
import sqlite3
from logger import logger
import re
import time
from db import check_db, series_exists, init_db
from utils import download_image
from config import BASE_URL, DATABASE_PATH, REQUEST_TIMEOUT, USER_AGENT, SLEEP_INTERVAL

def scrape_series_details(series_url):
    try:
        response = requests.get(f"{BASE_URL}{series_url}", timeout=REQUEST_TIMEOUT, headers={'User-Agent': USER_AGENT})
        if response.status_code != 200:
            logger.error(f"Failed to fetch details page {series_url}: Status {response.status_code}")
            return None, None, None, None, None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract release date
        release_date = None
        info_list = soup.select('ul.list-inline.list-separator.fs-xs.text-gray-500.mb-1 li.list-inline-item')
        if info_list:
            release_date = info_list[0].text.strip()
        
        # Extract country
        country = None
        country_elem = soup.select_one('h2.fs-base.mb-3.fw-normal.text-gray-600')
        if country_elem:
            country = country_elem.text.strip()
        
        # Extract description
        description = None
        desc_elem = soup.select_one('p.fs-sm.text-muted[data-more]')
        if desc_elem:
            description = desc_elem.text.strip()
        
        # Extract all categories
        categories = []
        category_elems = soup.select('div.card-tag a')
        for elem in category_elems:
            category = elem.text.strip()
            if category:
                categories.append(category)
        category_str = ', '.join(categories) if categories else None
        
        # Extract trailer link
        trailer_link = None
        trailer_elem = soup.select_one('a.btn.btn-stream.btn-ghost.btn-sm:contains("Watch trailer")')
        if trailer_elem and 'href' in trailer_elem.attrs:
            trailer_link = trailer_elem['href']
        
        return release_date, description, country, category_str, trailer_link
    except Exception as e:
        logger.error(f"Error scraping details for {series_url}: {e}")
        return None, None, None, None, None

def scrape_series():
    # Check if database is valid before scraping
    if not check_db():
        logger.error("Database check failed, aborting scrape")
        return
    
    base_url = f"{BASE_URL}/series"
    page = 1
    save_dir = "data/images/series"
    
    while True:
        url = f"{base_url}?genre=&release=1950;2025&rating=5;10&sorting=newest&language=&page={page}"
        logger.info(f"Scraping page {page}: {url}")
        
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT, headers={'User-Agent': USER_AGENT})
            if response.status_code != 200:
                logger.error(f"Failed to fetch page {page}: Status {response.status_code}")
                break
            
            soup = BeautifulSoup(response.text, 'html.parser')
            series_cards = soup.select('div.col-lg-2 a.card-movie')
            
            if not series_cards:
                logger.info("No more series found, stopping pagination")
                break
            
            conn = sqlite3.connect(DATABASE_PATH)
            c = conn.cursor()
            
            for card in series_cards:
                try:
                    # Extract title
                    title_elem = card.select_one('h3.title')
                    title = title_elem.text.strip() if title_elem else None
                    if not title:
                        logger.warning("Skipping series card with no title")
                        continue
                    
                    # Check if series already exists
                    if series_exists(title):
                        logger.info(f"Series already exists in database, skipping: {title}")
                        continue
                    
                    # Extract image URL
                    image_elem = card.select_one('img')
                    image_url = image_elem['src'] if image_elem else None
                    
                    # Extract IMDb rating
                    imdb_elem = card.select_one('div.card-imdb span')
                    imdb = imdb_elem.text.strip() if imdb_elem else None
                    
                    # Extract year
                    year = None
                    ul_elem = card.select_one('ul.list-inline')
                    if ul_elem:
                        items = ul_elem.find_all('li')
                        if len(items) >= 2:
                            year = items[1].text.strip()
                        elif len(items) == 1:
                            year = items[0].text.strip()
                    
                    # Get series detail page URL
                    series_url = card['href']
                    
                    # Scrape additional details
                    release_date, description, country, category, trailer_link = scrape_series_details(series_url)
                    
                    # Download and save image
                    image_path = download_image(image_url, title, save_dir) if image_url else None
                    
                    # Insert into database
                    c.execute('''INSERT OR IGNORE INTO series 
                                (title, image, year, imdb, release_date, description, country, category, trailer_link)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                              (title, image_path, year, imdb, release_date, description, country, category, trailer_link))
                    logger.info(f"Inserted series: {title}")
                    
                except Exception as e:
                    logger.error(f"Error processing series card: {e}")
                    continue
            
            conn.commit()
            conn.close()
            logger.debug("Database connection closed for page")
            
            # Check for next page
            next_page = soup.select_one('ul.pagination a.page-link[href*="page=' + str(page + 1) + '"]')
            if not next_page:
                logger.info("No next page found, stopping")
                break
            
            page += 1
            time.sleep(SLEEP_INTERVAL)  # Be polite to the server
            
        except Exception as e:
            logger.error(f"Error scraping page {page}: {e}")
            break
    
    logger.info("Series scraping completed")

if __name__ == "__main__":
    init_db()
    scrape_series()