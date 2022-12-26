from core.extractors.company import Company
from core.extractors.person import Person
from datetime import timedelta
from functools import wraps
from core.actions import *
import pandas as pd
import random
import time

MAX_PAGES_PER_ACCOUNT = 200


class LinkedinScraper:
    count = 0

    def __init__(self):
        self.driver = get_chrome_driver()
        login(self.driver)

    @staticmethod
    def check_account(func):
        @wraps(func)
        def wrapper(*args, **kw):
            self = args[0]
            if self.count == MAX_PAGES_PER_ACCOUNT:
                self.driver.close()
                self.driver = get_chrome_driver()
                self.count = 0
                login(self.driver)

            res = func(*args, **kw)
            self.count += 1

            return res

        return wrapper

    def load_extractors(self):
        pass

    @check_account
    def get_company_from_employee(self):
        pass

    @check_account
    def get_company_by_name(self):
        print(self.count)
        pass

    @check_account
    def get_company_by_link(self, company_url: str) -> Company:
        return Company(self.driver, company_url)

    @check_account
    def get_person(self, url: str) -> Person:
        return Person(self.driver, url)

    def test_csv(self, csv_path: str):
        df = pd.read_csv(csv_path)
        start = time.time()
        successfully = list()
        for index, row in df.iterrows():
            try:
                if index != 0:
                    time.sleep(random.randint(2, 4))
                    successfully.append(Company(self.driver, row["Linkedin"]))
            except Exception as ex:
                logger.exception(ex)
                break

        end = time.time()
        logger.info(
            f"Tempo total : {timedelta(seconds=end - start)}s | Contagem Test {len(successfully)}"
        )

