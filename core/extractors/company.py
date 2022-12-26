from .objects import Experience, Education, Interest, Accomplishment, Contact
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from selenium import webdriver
from bs4 import BeautifulSoup
from loguru import logger
from time import time
import regex as re
import typing as t
import os


@dataclass
class CompanySummary:
    pass


class Company:
    WAIT_FOR_ELEMENT_TIMEOUT = 5

    def __init__(self, driver: webdriver.Chrome, url: str):
        self.driver = driver
        self.url = url
        self.linkedin_url = None
        self.name = None
        self.about_us = None
        self.website = None
        self.headquarters = None
        self.founded = None
        self.industry = None
        self.company_type = None
        self.company_size = None
        self.specialties = None
        self.showcase_pages = []
        self.affiliated_companies = []
        self.employees = []
        self.headcount = None
        self.errors = []

        self.driver.get(url)
        self._set_company_properties()

    @staticmethod
    def _find_first_available_element(*args) -> WebElement:
        for element in args:
            if element:
                return element[0]

    def _set_about_us(self):
        WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.XPATH, '//span[@dir="ltr"]'))
        )

        # Access about us through the page element
        try:
            navigation = self.driver.find_element(
                By.CLASS_NAME, "org-page-navigation__items"
            )
            self._find_first_available_element(
                navigation.find_elements(
                    By.XPATH, "//a[@data-control-name='page_member_main_nav_about_tab']"
                ),
                navigation.find_elements(
                    By.XPATH,
                    "//a[@data-control-name='org_about_module_see_all_view_link']",
                ),
            ).click()
        # Try to access through the url
        except:
            company_about_url = os.path.join(self.url, "about")
            self.driver.get(company_about_url)

        WebDriverWait(self.driver, 3).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "section"))
        )

        grid = self.driver.find_element(By.CLASS_NAME, "artdeco-card.p5.mb4")
        desc_wrapper = grid.find_elements(By.TAG_NAME, "p")

        if len(desc_wrapper) > 0:
            self.about_us = desc_wrapper[0].text.strip()

        labels = grid.find_elements(By.TAG_NAME, "dt")
        values = grid.find_elements(By.TAG_NAME, "dd")
        num_attributes = min(len(labels), len(values))
        x_off = 0

        for i in range(num_attributes):
            txt = labels[i].text.strip()
            if txt == "Website":
                self.website = values[i + x_off].text.strip()
            elif txt == "Industry":
                self.industry = values[i + x_off].text.strip()
            elif txt == "Company size":
                self.company_size = values[i + x_off].text.strip()
                if len(values) > len(labels):
                    x_off = 1
            elif txt == "Headquarters":
                self.headquarters = values[i + x_off].text.strip()
            elif txt == "Type":
                self.company_type = values[i + x_off].text.strip()
            elif txt == "Founded":
                self.founded = values[i + x_off].text.strip()
            elif txt == "Specialties":
                self.specialties = "\n".join(values[i + x_off].text.strip().split(", "))

    def _set_name(self):
        self.name = self.driver.find_element(
            By.XPATH, '//span[@dir="ltr"]'
        ).text.strip()

    def _set_company_properties(self):
        self._set_name()
        self._set_about_us()
        self._check_company_properties()

    def _check_company_properties(self):
        pass
