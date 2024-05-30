from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class SeleniumUtils:
    def __init__(self):
        self.__options = self.__configure_chrome_options()
        self.timeout = 30
    
    def get_chrome_driver(self, proxy=None):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.__options)
        return driver
    
    def __configure_chrome_options(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach",True)
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--js-flags="--expose-gc"')
        options.add_argument('--enable-precise-memory-info')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--log-level=3')
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        return options

    def actions__get_all_elements(self, by, locator, driver):
        try:
            elements = Wait(driver, self.timeout).until(EC.presence_of_all_elements_located((by, locator)))
            return elements
        except Exception as e:
            print(e)
            return False
        
    def actions__find_element(self, by, locator, driver):
        try:
            element = Wait(driver, self.timeout).until(EC.presence_of_element_located((by, locator)))
            return element
        except Exception as e:
            print(e)
            return False

    def actions__click_element(self, by, locator, driver):
        try:
            element = Wait(driver, self.timeout).until(EC.presence_of_element_located((by, locator))).click()
        except Exception as e:
            print(e)
            return False

    def actions__send_keys(self, by, locator, keys, driver):
        try:
            element = Wait(driver, self.timeout).until(EC.presence_of_element_located((by, locator))).send_keys(keys)
            return element
        except Exception as e:
            print(e)
            return False