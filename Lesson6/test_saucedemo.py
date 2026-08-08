import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ——— Page Objects ———

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    USERNAME  = (By.ID, "user-name")
    PASSWORD  = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")

    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def success_login(self, username, password):
        # element_to_be_clickable лучше чем presence — поле точно видимо и кликабельно
        self.wait.until(EC.element_to_be_clickable(self.USERNAME)).send_keys(username)
        self.wait.until(EC.element_to_be_clickable(self.PASSWORD)).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BTN)).click()


class InventoryPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def add_item_to_cart(self, item_name):   # ← добавить недостающий метод!
        button_xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
        self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath))).click()

    def go_to_cart(self):
        self.wait.until(EC.element_to_be_clickable(self.CART_LINK)).click()


class CartPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    CHECKOUT_BTN = (By.ID, "checkout")   # ← вынести локатор в переменную

    def proceed_to_checkout(self):
        self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BTN)).click()


class CheckoutPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    
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


# ——— Фикстура ———

@pytest.fixture(scope="class")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


# ——— Тестовый класс ———

class TestCheckout:
    @pytest.fixture(scope="class", autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        self.inventory_page = InventoryPage(driver)
        self.cart_page = CartPage(driver)
        self.checkout_page = CheckoutPage(driver)

    def test_checkout_total_price(self):
        self.login_page.open()
        self.login_page.success_login("standard_user", "secret_sauce")
        self.inventory_page.add_item_to_cart("Sauce Labs Backpack")
        self.inventory_page.add_item_to_cart("Sauce Labs Bolt T-Shirt")
        self.inventory_page.add_item_to_cart("Sauce Labs Onesie")
        self.inventory_page.go_to_cart()
        self.cart_page.proceed_to_checkout()
        self.checkout_page.fill_checkout_form("Anna", "Smith", "12345")

        total = self.checkout_page.get_total_price()
        assert total == "$58.29", f"Итоговая сумма неверна: {total}"