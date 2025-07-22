from scraper.service import LeagueOfGraphsScraperService

def provide_scraper():
    scraper = LeagueOfGraphsScraperService()

    yield scraper
    # anything that needs to be executed after the function that's being injected with this dependency should go here
    # for example, closing a db connection

