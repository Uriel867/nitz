from scraper.service import LeagueOfGraphsScraper

def provide_scraper():
    scraper = LeagueOfGraphsScraper()

    yield scraper
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

