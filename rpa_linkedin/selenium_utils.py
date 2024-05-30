from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as Wait

class SeleniumUtils:
    def get_element(self, driver, by, value):
        try:
            element = Wait(driver, 5).until(EC.visibility_of_element_located((by, value)))
            return element
        except Exception as e:
            return False
