from scraper.service import TrackerGGScraper

def get_scraper():
    scraper = TrackerGGScraper()

    yield scraper
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

