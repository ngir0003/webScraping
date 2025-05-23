import sqlite3
from pathlib import Path
from logger import logger
from config import DATABASE_PATH

def check_db():
    """Check if the database exists and has the correct schema for movies and series tables."""
    db_path = DATABASE_PATH
    required_columns = {
        'movies': [
            ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
            ('title', 'TEXT'),
            ('image', 'TEXT'),
            ('year', 'TEXT'),
            ('imdb', 'TEXT'),
            ('release_date', 'TEXT'),
            ('description', 'TEXT'),
            ('country', 'TEXT'),
            ('category', 'TEXT'),
            ('trailer_link', 'TEXT')
        ],
        'series': [
            ('id', 'INTEGER PRIMARY KEY AUTOINCREMENT'),
            ('title', 'TEXT'),
            ('image', 'TEXT'),
            ('year', 'TEXT'),
            ('imdb', 'TEXT'),
            ('release_date', 'TEXT'),
            ('description', 'TEXT'),
            ('country', 'TEXT'),
            ('category', 'TEXT'),
            ('trailer_link', 'TEXT')
        ]
    }

    logger.info(f"Checking database at {db_path}")
    
    # Check if database file exists
    if not db_path.exists():
        logger.warning(f"Database {db_path} does not exist")
        init_db()
        return True

    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Check if tables exist and migrate if necessary
        for table in ['movies', 'series']:
            c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not c.fetchone():
                logger.warning(f"{table} table does not exist")
                init_db()
                conn.close()
                return True

            # Check columns
            c.execute(f"PRAGMA table_info({table})")
            existing_columns = {(row[1], row[2]) for row in c.fetchall()}
            required_columns_set = {(name, type_) for name, type_ in required_columns[table]}
            
            if existing_columns != required_columns_set:
                logger.warning(f"{table} table schema mismatch. Expected: {required_columns_set}, Found: {existing_columns}")
                # Check if only trailer_link is missing
                missing_columns = required_columns_set - existing_columns
                if missing_columns == {('trailer_link', 'TEXT')}:
                    logger.info(f"Adding trailer_link column to {table} table")
                    c.execute(f"ALTER TABLE {table} ADD COLUMN trailer_link TEXT")
                    conn.commit()
                    logger.info(f"Successfully added trailer_link to {table}")
                else:
                    logger.error(f"Schema mismatch beyond trailer_link. Reinitializing database.")
                    init_db()
                    conn.close()
                    return True

        conn.close()
        logger.info("Database and tables schema verified successfully")
        return True
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error checking {db_path}: {e}")
        conn.close()
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking database: {e}")
        conn.close()
        return False

def exists_in_table(table, title):
    """Check if an item with the given title exists in the specified table."""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        c = conn.cursor()
        c.execute(f"SELECT 1 FROM {table} WHERE title = ?", (title,))
        exists = c.fetchone() is not None
        conn.close()
        logger.debug(f"Checked {table} existence: {title} {'exists' if exists else 'does not exist'}")
        return exists
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error checking {table} existence for {title}: {e}")
        conn.close()
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking {table} existence for {title}: {e}")
        conn.close()
        return False

def movie_exists(title):
    """Check if a movie with the given title exists in the movies table."""
    return exists_in_table('movies', title)

def series_exists(title):
    """Check if a series with the given title exists in the series table."""
    return exists_in_table('series', title)

def init_db():
    """Initialize the database with movies and series tables."""
    db_path = DATABASE_PATH
    logger.info(f"Initializing database at {db_path}")
    try:
        # Ensure parent directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        logger.debug("Creating 'movies' table if not exists")
        c.execute('''CREATE TABLE IF NOT EXISTS movies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        image TEXT,
                        year TEXT,
                        imdb TEXT,
                        release_date TEXT,
                        description TEXT,
                        country TEXT,
                        category TEXT,
                        trailer_link TEXT
                    )''')
        
        logger.debug("Creating 'series' table if not exists")
        c.execute('''CREATE TABLE IF NOT EXISTS series (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        image TEXT,
                        year TEXT,
                        imdb TEXT,
                        release_date TEXT,
                        description TEXT,
                        country TEXT,
                        category TEXT,
                        trailer_link TEXT
                    )''')
        
        conn.commit()
        logger.info("Database initialized successfully")
    except sqlite3.DatabaseError as e:
        logger.error(f"Failed to initialize database: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error initializing database: {e}")
        raise
    finally:
        conn.close()
        logger.debug("Database connection closed")