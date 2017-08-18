## OLX Real Estate Listing Crawler
### Dependencies
Python3.6, virtualenv (optional), sqlite3
### Setting up
- Install Python dependencies by running `pip install -r requirements.txt`
- Run `python sql/setup_db.py`
### Running the crawler
- Run `./scripts/crawl.sh <pages>`, where `pages` is the number of pages you want to crawl. This defaults to 100.
