from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DATABASE_PATH = BASE_DIR / "data" / "database" / "movies_series.db"

# Directory paths
DIRECTORIES = [
    BASE_DIR / "data" / "database",
    BASE_DIR / "data" / "images" / "movies",
    BASE_DIR / "data" / "images" / "series",
    BASE_DIR / "logs",
]

# Scraper configuration
BASE_URL = "https://uflix.to"
REQUEST_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
SLEEP_INTERVAL = 1  # Seconds between page requests