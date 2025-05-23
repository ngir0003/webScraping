import requests
import re
from logger import logger
from config import BASE_URL, REQUEST_TIMEOUT, USER_AGENT

def download_image(image_url, title, save_dir):
    try:
        # Sanitize title to create a valid filename
        safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_').lower()
        image_name = f"{safe_title}.jpg"
        image_path = f"{save_dir}/{image_name}"
        
        # Ensure the directory exists
        import os
        os.makedirs(save_dir, exist_ok=True)
        
        # Download the image
        full_url = f"{BASE_URL}{image_url}" if not image_url.startswith('http') else image_url
        response = requests.get(full_url, stream=True, timeout=REQUEST_TIMEOUT, headers={'User-Agent': USER_AGENT})
        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            logger.info(f"Downloaded image for {title} to {image_path}")
            return image_path
        else:
            logger.error(f"Failed to download image for {title}: Status {response.status_code}")
            return None
    except Exception as e:
        logger.error(f"Error downloading image for {title}: {e}")
        return None