import logging

import requests
from bs4 import BeautifulSoup

import settings

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s][%(asctime)s][%(filename)s][%(lineno)s]: %(message)s",
    datefmt="%H:%M:%S",
    filename="logs.txt",
)


class Scraper:
    def __init__(self):
        self.client = requests.Session()

    def make_request(self, url, method, params={}):

        self.response = self.client.request(method, url, data=params)

        logging.debug(f"Response's status code: {self.response.status_code}")
        logging.debug(f"Response's content: {self.response.content}")

    def make_soup(self):

        if self.response.status_code == 200:
            self.soup = BeautifulSoup(self.response.content, "html.parser")
        else:
            logging.error(
                "Expected status code 200, but got {}".format(self.response.status_code)
            )
            raise requests.ConnectionError(
                "Expected status code 200, but got {}".format(self.response.status_code)
            )

    def get_token(self):

        self.make_request(url="https://parascrapear.com/login", method="GET")

        self.make_soup()

        self.crsf_token = self.soup.find("input", {"name": "csrf_token"}).get("value")

        logging.debug("El token CRSF es: {}".format(self.crsf_token))

        return self.crsf_token

    def make_login(self):

        self.credentials = settings.LOGIN_CREDENTIALS
        self.credentials["csrf_token"] = self.crsf_token

        self.make_request(
            url="https://parascrapear.com/login", 
            method="POST", 
            params=self.credentials
        )

    def is_logged(self):

        self.make_soup()

        toptext = self.soup.find(id="toptext").text
        logging.debug(str(toptext))

        if "Cerrar sesión" in toptext:
            return True

        else:
            return False

    def get_page_post_login(self):

        self.make_request(url="https://parascrapear.com", method="GET")

        self.make_soup()

        return self.soup
