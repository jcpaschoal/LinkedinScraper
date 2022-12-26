from .objects import Experience, Education, Interest, Accomplishment, Contact
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from loguru import logger
import regex as re


class Person:
    WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver

        self.name = None
        self.about = []
        self.experiences = []
        self.educations = []
        self.contacts = []
        self.accomplishments = []
        self.also_viewed_urls = []
        self.interests = []
        self.href = []
        self.location = []

        self.driver.get(url)
        self._set_all()

    def _set_name(self):
        try:
            root = WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        "pv-top-card",
                    )
                )
            )

            self.name = root.find_element(
                By.CLASS_NAME, "text-heading-xlarge"
            ).text.strip()
        except TimeoutError as e:
            pass

    def _set_about(self):
        # Quebrando em alguns tipos de perfil privado
        try:
            see_more = WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "inline-show-more-text__button")
                )
            )
            self.driver.execute_script("arguments[0].click();", see_more)

            about = WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        "pv-shared-text-with-see-more",
                    )
                )
            )
            if about:
                self.about.append(about.text.strip())
        except TimeoutError:
            self.about = None

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    @staticmethod
    def _href_validator(link: str, type_href: str):
        regex = re.search(
            r"https:\/\/www.linkedin.com\/in\/.+\/details\/{}\?profile.+".format(
                type_href
            ),
            link,
        )
        if regex:
            return regex.group(0)

    @staticmethod
    def _set_experience(self):
        pass

    def _set_education(self):
        pass

    def _set_href(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        for a in soup.find_all("a"):
            self.href.append(a["href"])

    def _set_all(self):
        self._set_name()
        self._set_about()
        self._set_href()

        self.driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )

        # get experience
        self.driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight*3/5));"
        )

        self.driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/1.5));"
        )

    @staticmethod
    def get_company_from_employee(driver: webdriver.Chrome, url: str):
        pass