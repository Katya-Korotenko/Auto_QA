from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CartPage(BasePage):
    CHECKOUT_BTN = (By.ID, "checkout")

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()