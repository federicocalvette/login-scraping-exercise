from scraper import Scraper

if __name__ == "__main__":

    scraper = Scraper()

    crsf_token = scraper.get_token()

    if not scraper.is_logged():

        scraper.make_login()

        print(scraper.get_page_post_login())
