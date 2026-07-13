from selenium import webdriver
from selenium.webdriver.common.by import By
import pytest



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://uitestingplayground.com/textinput")
    driver.implicitly_wait(15)
    yield driver
    driver.quit()




def test_text_input(driver):
    field = driver.find_element(By.ID, "newButtonName")
    field.send_keys("ITCH")
    button = driver.find_element(By.CSS_SELECTOR, ".btn-primary")
    button.click()
    assert button.text == "ITCH"