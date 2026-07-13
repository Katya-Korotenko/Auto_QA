import pytest, time
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    yield driver
    driver.quit()

def test_first_cat_card_is_displayed(driver):
    # driver.implicitly_wait(5)
    driver.get('https://suninjuly.github.io/cats.html')
    first_cat_card = driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(2)")
    assert first_cat_card.is_displayed()

def test_first_2_cat_card_is_displayed(driver):
    # driver.implicitly_wait(15)
    driver.get('https://suninjuly.github.io/cats.html')
    first_cat_card = driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(3)")
    assert first_cat_card.is_displayed()

def test_first_3_cat_card_is_displayed(driver):
    driver.implicitly_wait(30)
    driver.get('https://suninjuly.github.io/cats.html')
    first_cat_card = driver.find_element(By.CSS_SELECTOR, ".col-sm-4:nth-child(3)")
    assert first_cat_card.is_displayed()