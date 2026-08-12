from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME  = (By.ID, "last-name")
    ZIP_CODE   = (By.ID, "postal-code")
    CONTINUE   = (By.ID, "continue")
    TOTAL      = (By.CLASS_NAME, "summary_total_label")

    def fill_checkout_form(self, first, last, zip_code):
        self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME)).send_keys(first)
        self.wait.until(EC.element_to_be_clickable(self.LAST_NAME)).send_keys(last)
        self.wait.until(EC.element_to_be_clickable(self.ZIP_CODE)).send_keys(zip_code)
        self.wait.until(EC.element_to_be_clickable(self.CONTINUE)).click()

    def get_total_price(self):
        return self.wait.until(
            EC.presence_of_element_located(self.TOTAL)
        ).text.replace("Total: ", "")