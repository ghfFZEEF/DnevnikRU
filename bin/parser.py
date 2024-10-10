import abc
from time import sleep

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class BasicParser(abc.ABC):
    @abc.abstractmethod
    def __init__(self, xpath: dict["login": str, "password": str, "button": str, "period": str]) -> None:
        pass

    @abc.abstractmethod
    def get_html(self, cookies: list[dict], school_schooler_num: tuple["school_num": int, "schooler_num": int]) -> str | bool:
        pass
    
    @abc.abstractmethod
    def get_cookies_school_schooler_num(self, login: str, password: str) -> tuple["cookies": dict, "school_schooler_num": tuple["school_num": int, "schooler_num": int]] | bool:
        pass


class SeleniumParser(BasicParser):
    def __init__(self, xpath: dict["login": str, "password": str, "button": str, "period": str]) -> None:
        self.__xpath: dict = xpath

    def get_html(self, cookies: list[dict], school_schooler_num: tuple["school_num": int, "schooler_num": int]) -> str | bool:
        driver: webdriver = self.__get_registered_driver_by_cookies(cookies)
        
        driver.get(f"https://dnevnik.ru/marks/school/{school_schooler_num[0]}/student/{school_schooler_num[1]}/period")

        # page_loaded: str = None
        # while page_loaded != "complete":
        #     page_loaded = driver.execute_script("return document.readyState")

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

        try:
            table: WebElement = driver.find_element(By.CLASS_NAME, "Tamh1")
        except NoSuchElementException:
            driver.quit()
            return False

        html: str = table.get_attribute("innerHTML")

        driver.quit()
        return html

    def __get_registered_driver_by_cookies(self, cookies: list[dict]) -> webdriver:
        driver: webdriver = webdriver.Chrome()
        driver.maximize_window()
        
        url: str = "https://login.dnevnik.ru/login/esia/rostov"
        driver.get(url)
        
        for cookie in cookies:
            driver.add_cookie(cookie)
    
        return driver
    
    def get_cookies_school_schooler_num(self, login: str, password: str) -> tuple["cookies": list[dict], "school_schooler_num": tuple["school_num": int, "schooler_num": int]] | bool:
        options: webdriver.ChromeOptions = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        url: str = "https://login.dnevnik.ru/login/esia/rostov"
        driver.get(url)

        driver = self.__get_registered_driver_by_log_pas(driver, login, password)
        
        if driver.current_url != "https://dnevnik.ru/userfeed":
            driver.quit()
            return False
        
        cookies: dict = driver.get_cookies()
        
        url: str = "https://dnevnik.ru/marks"
        driver.get(url)
        driver.find_element(By.XPATH, self.__xpath["period"]).click() 
        url: list = driver.current_url.split('/')
        school_schooler_num: tuple = (url[5], url[7])
        
        driver.quit()
        return (cookies, school_schooler_num)
        
    def __get_registered_driver_by_log_pas(self, driver: webdriver, login: str, password: str) -> webdriver:
        login_entry = driver.find_element(By.XPATH, self.__xpath["login"])
        password_entry = driver.find_element(By.XPATH, self.__xpath["password"])
        login_entry.send_keys(login)
        password_entry.send_keys(password)
        driver.find_element(By.XPATH, self.__xpath["button"]).click()
        
        return driver
    