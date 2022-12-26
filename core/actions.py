from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from speech_recognition import Recognizer, AudioFile
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from dataclasses import dataclass
from selenium import webdriver
from core.proxies import PROXIES
from loguru import logger
import random
import urllib
import os

DRIVER_OPTIONS = {"prod": ["--headless", "--no-sandbox"]}


@dataclass
class LoginCredentials:
    email: str
    password: str

    def __post_init__(self):
        if not self.email or not self.password:
            raise Exception("Credentials cannot be null")


def get_chrome_driver(env: str = "test"):
    chrome_options = Options()
    random_proxy = random.choice(PROXIES)
    chrome_options.add_argument('--proxy-server=%s' % random_proxy)

    if (arguments := DRIVER_OPTIONS.get(env)) is not None:
        for argument in arguments:
            chrome_options.add_argument(argument)

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )


def get_login_credentials() -> LoginCredentials:
    user = os.environ.get("LINKEDIN_USER", None)
    password = os.environ.get("LINKEDIN_PASSWORD", None)
    return LoginCredentials(user, password)


def puzzle_solver() -> str:
    pass


def email_solver(email: str, password: str) -> str:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.gmx.com")
    try:
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "permission-core-iframe")))
        driver.switch_to.frame(driver.find_element(By.XPATH, "//iframe"))
        driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        driver.find_element(By.ID, "login-button").click()
        email_elem = driver.find_element(By.ID, "login-email")
        email_elem.send_keys(email)
        password_elem = driver.find_element(By.ID, "login-password")
        password_elem.send_keys(password)
        password_elem.submit()

    except TimeoutException as ex:
        pass


def login(driver: webdriver.Chrome, cookie: str = None, timeout: int = 10):
    if cookie is not None:
        driver.get("https://www.linkedin.com/login")
        driver.add_cookie({"name": "li_at", "value": cookie})

    credentials = get_login_credentials()
    logger.info(f"Logging in as :{credentials.email}")
    driver.get("https://www.linkedin.com/login")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
    email_elem = driver.find_element(By.ID, "username")
    email_elem.send_keys(credentials.email)
    password_elem = driver.find_element(By.ID, "password")
    password_elem.send_keys(credentials.password)
    password_elem.submit()

    try:
        if driver.current_url == "https://www.linkedin.com/checkpoint/lg/login-submit":
            remember = driver.find_element(By.ID, "remember-me-prompt__form-primary")
            if remember:
                remember.submit()

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "global-nav-search"))
        )
    except TimeoutException as ex:
        pass



