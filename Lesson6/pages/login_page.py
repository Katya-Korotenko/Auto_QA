from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME  = (By.ID, "user-name")
    PASSWORD  = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")


    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def success_login(self, username, password):
        self.wait.until(EC.element_to_be_clickable(self.USERNAME)).send_keys(username)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()