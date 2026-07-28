# test_shop.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


# ——— Page Objects ———

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    USERNAME  = (By.ID, "user-name")
    PASSWORD  = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")

    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, username, password):
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BTN).click()


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver

    BACKPACK_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    TSHIRT_BTN   = (By.ID, "add-to-cart-sauce-labs-bolt-t-shirt")
    ONESIE_BTN   = (By.ID, "add-to-cart-sauce-labs-onesie")
    CART_LINK    = (By.CLASS_NAME, "shopping_cart_link")

    def add_items(self):
        self.driver.find_element(*self.BACKPACK_BTN).click()
        self.driver.find_element(*self.TSHIRT_BTN).click()
        self.driver.find_element(*self.ONESIE_BTN).click()

    def go_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()


class CartPage:
    def __init__(self, driver):
        self.driver = driver

    CHECKOUT_BTN = (By.ID, "checkout")

    def checkout(self):
        self.driver.find_element(*self.CHECKOUT_BTN).click()


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME  = (By.ID, "last-name")
    ZIP_CODE   = (By.ID, "postal-code")
    CONTINUE   = (By.ID, "continue")
    TOTAL      = (By.CLASS_NAME, "summary_total_label")

    def fill_form(self, first, last, zip_code):
        self.driver.find_element(*self.FIRST_NAME).send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        self.driver.find_element(*self.ZIP_CODE).send_keys(zip_code)
        self.driver.find_element(*self.CONTINUE).click()

    def get_total(self):
        return self.driver.find_element(*self.TOTAL).text


# ——— Фикстура и тест ———

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


def test_checkout(driver):
    LoginPage(driver).open()
    LoginPage(driver).login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_items()
    inventory.go_to_cart()

    CartPage(driver).checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_form("Anna", "Smith", "12345")

    total = checkout.get_total()
    assert total == "Total: $58.29"