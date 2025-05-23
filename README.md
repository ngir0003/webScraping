# WebScraping

WebScraping is a Python-based tool that scrapes movie and series metadata (titles, posters, release dates, genres, IMDb ratings, descriptions, countries, trailer links) from [uflix.to](https://uflix.to) and stores it in a SQLite database. Ideal for developers and data enthusiasts for media cataloging or analysis.

## Features

- Extracts movie/series data: titles, posters, years, IMDb ratings, release dates, descriptions, countries, genres, trailers.
- Stores data in `movies_series.db`.
- Downloads posters to `data/images/`.
- Handles errors and logs to `logs/movies_series.log`.
- Modular code with automated setup.

## Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/ngir0003/webScraping.git
   cd webScraping
   ```

2. Set up virtual environment (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Run setup script:
   ```bash
   python setup_project.py
   ```
   Installs dependencies, creates directories (`data/database/`, `data/images/`, `logs/`), and initializes `movies_series.db`.

## Usage

1. Scrape data:
   ```bash
   python get_movies_series.py
   ```
   Scrapes data, stores it in `movies_series.db`, downloads posters, and logs to `logs/movies_series.log`.

2. View database:
   Use an SQLite client (e.g., [DB Browser for SQLite](https://sqlitebrowser.org/)) to query `data/database/movies_series.db`.

## Project Structure

```
webScraping/
├── movies.py              # Movie data scraper
├── series.py              # Series data scraper
├── get_movies_series.py   # Main script
├── db.py                  # Database management
├── utils.py               # Utilities (e.g., image downloading)
├── logger.py              # Logging setup
├── config.py              # Configuration
├── setup_project.py       # Setup script
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── data/
    ├── database/
    │   └── movies_series.db
    └── images/
        ├── movies/
        └── series/
```

## Dependencies

- `requests==2.32.3`
- `beautifulsoup4==4.12.3`

Install:
```bash
pip install -r requirements.txt
```

## Contributing

1. Fork: [https://github.com/ngir0003/webScraping.git](https://github.com/ngir0003/webScraping.git)
2. Create branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/your-feature`
5. Open a Pull Request.

## Issues

Report bugs/features via [GitHub Issues](https://github.com/ngir0003/webScraping/issues).

## License

Licensed under the [Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0).

## Author

Nicholas Girdlestone ([ngir0003](https://github.com/ngir0003))

⭐ Star this repo if you find it useful!