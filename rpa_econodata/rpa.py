from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
from selenium_utils import SeleniumUtils
from  rpa_utils import WebScraperUtils
import time
import json
import os
import datetime

# Load environment variables from the .env file
load_dotenv()

class WebScraper:
    def __init__(self):   
        self.selenium = SeleniumUtils()
        self.utils = WebScraperUtils()

        self.list_company = []

        self.__iteration_limit = 100
        self.__last_iteration = None
        self.__xlsx_count = 0
        self.__total_iterations = 1815

    def scraper_login(self, driver):
        driver.get("https://plat.econodata.com.br/?_gl=1*7pjh8j*_ga*MTcxNzE5NjEyNi4xNzE1MTk3MzQx*_ga_BFMKLBFXM8*MTcxNTYyODMwNC4xLjAuMTcxNTYyODMwNC42MC4wLjA.#/login")
        self.selenium.actions__send_keys(
            By.XPATH,
            '//*[@id="E-mail"]', 
            [os.getenv("USER_NAME"), Keys.TAB, os.getenv("USER_PASSWORD"), Keys.TAB, Keys.TAB, Keys.ENTER],
            driver
        )

    def select_default_filter(self, driver):   
        saved_searches = self.selenium.actions__click_element(By.XPATH,"/html/body/div[3]/div[1]/div/nav/section/ul/li[9]/a", driver)
        if saved_searches is False:
            return False

        time.sleep(2)
        search = self.selenium.actions__click_element(By.XPATH,'//*[@id="tableIndividual"]/tbody/tr[1]/td[4]/div/button[2]', driver)
        
        if search is False:
            return False

        select_element = self.selenium.actions__find_element(By.XPATH, '//*[@id="perPageSelect"]', driver)
        Select(select_element).select_by_value("250")
        time.sleep(2)

        return True

    def scraper_companies(self, driver):
        # pag = 1

        # while True:
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        rows = self.selenium.actions__get_all_elements(By.CSS_SELECTOR, 'tr.ecdt-tr', driver)

        current_list_iteration = len(self.list_company) + 1

        for idx, row in enumerate(rows):
            if self.__xlsx_count > idx:
                continue

            row.click()
            time.sleep(3)

            print(f'{len(self.list_company)} - {datetime.datetime.now()}')

            if current_list_iteration % self.__iteration_limit == 0:
                return

            cnpj = self.selenium.actions__find_element(By.XPATH, "/html/body/div[3]/div[1]/main/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div/span[1]", driver)
            already_in_file = self.utils.cnpj_exists(cnpj.text)
            if already_in_file is True:
                current_list_iteration = len(self.list_company) + 1
                self.selenium.actions__click_element(By.XPATH, "/html/body/div[3]/div[1]/main/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/button", driver)
                continue

            money = self.selenium.actions__find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div/div/div[3]/div[3]/div[5]/div/span', driver)
            name = self.selenium.actions__find_element(By.XPATH, "/html/body/div[3]/div[1]/main/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]/h1", driver)

            self.selenium.actions__click_element(By.XPATH, '//*[@id="padding-container"]/div[2]/div/div/div[2]', driver)
            time.sleep(1)
            self.selenium.actions__click_element(By.CSS_SELECTOR, '#collapse-pessoas-emails li:nth-child(2)', driver)
            time.sleep(1)

            company_person_list = self.selenium.actions__get_all_elements(By.CSS_SELECTOR, '#collapse-pessoas-emails tr > td:nth-child(1)', driver)
            company_person_list_formatted = []

            if company_person_list is False:
                print(f"{name.text} - não possui decisores ou o XPATH está diferente")
            else:
                for company_person_el in company_person_list:
                    person_and_role = company_person_el.text.split('\n', 1)
                    person_name, person_role = person_and_role if len(person_and_role) > 1 else (person_and_role[0], "")
                    if person_name.strip() and person_role.strip():
                        company_person_list_formatted.append(f"{person_name} ({person_role})")

            self.list_company.append(
                {
                    "empresa": name.text,
                    "cnpj": cnpj.text,
                    "capital_social": money.text,
                    "pessoas": '\n'.join(company_person_list_formatted)
                }
            )

            current_list_iteration = len(self.list_company)

            self.selenium.actions__click_element(By.XPATH, "/html/body/div[3]/div[1]/main/div/div/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div[1]/button", driver)

            # self.navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(1)
            # element = self.selenium.actions__click_element(By.XPATH,"/html/body/div[3]/div[1]/main/div/div/div[3]/div[2]/div[2]/div[2]/div/div/div[3]/div/div/div[1]/ul/li[8]")
            # time.sleep(2)
            # pag += 1

    def scrape(self, driver):
        sucess_login = self.scraper_login(driver)
        if sucess_login is False:
            print(f"[sucess_login]: ERROR")
            return

        success_select_filter = self.select_default_filter(driver)
        if success_select_filter is False:
            print(f"[success_select_filter]: ERROR")
            return

        success_scraper_companies = self.scraper_companies(driver)
        if success_scraper_companies is False:
            print(f"[success_scraper_companies]: ERROR")
            return

    def startX(self):
        while self.__xlsx_count < self.__total_iterations:
            if (self.__last_iteration is None):
                print(f"carregando novo driver...")
                driver = self.selenium.get_chrome_driver()
                self.scrape(driver)
                driver.quit()
                
                print("salvando dados...")
                self.utils.xlsx_update(data=self.list_company)

                print("limpando lista...")
                self.list_company = []

                print("atualizando contagem xlsx...")
                self.__xlsx_count = self.utils.xlsx_size()

                print("recomeçando...")
                self.__last_iteration = None

robo = WebScraper()
robo.startX()