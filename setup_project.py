import requests
import subprocess
import sys
from logger import logger
from db import init_db, check_db
from config import DIRECTORIES, BASE_URL, REQUEST_TIMEOUT, USER_AGENT

def install_requirements():
    """Install dependencies from requirements.txt."""
    requirements_file = "requirements.txt"
    try:
        logger.info(f"Installing dependencies from {requirements_file}")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_file],
            check=True,
            capture_output=True,
            text=True
        )
        logger.info("Dependencies installed successfully")
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        logger.debug(e.stderr)
        raise
    except FileNotFoundError:
        logger.error(f"{requirements_file} not found in project directory")
        raise
    except Exception as e:
        logger.error(f"Unexpected error installing dependencies: {e}")
        raise

def create_directories():
    """Create necessary directories for the project."""
    try:
        for directory in DIRECTORIES:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
    except PermissionError as e:
        logger.error(f"Permission denied creating directory {directory}: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create directories: {e}")
        raise

def check_site_accessibility(url=BASE_URL):
    """Check if the target site is accessible."""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, timeout=REQUEST_TIMEOUT, headers=headers)
        if response.status_code == 200:
            logger.info(f"Site {url} is accessible")
            return True
        else:
            logger.warning(f"Site {url} returned status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Failed to access site {url}: {e}")
        return False

def setup_project():
    """Set up the project by installing dependencies, initializing the database, creating directories, and checking site accessibility."""
    logger.info("Starting project setup")
    
    # Install dependencies
    install_requirements()
    
    # Create directories
    create_directories()
    
    # Initialize and check database (triggers migration if needed)
    init_db()
    if not check_db():
        logger.error("Database setup or migration failed")
        raise Exception("Database setup or migration failed")
    
    # Check site accessibility
    if not check_site_accessibility():
        logger.warning("Site accessibility check failed, but continuing setup")
    
    logger.info("Project setup completed successfully")

if __name__ == "__main__":
    setup_project()