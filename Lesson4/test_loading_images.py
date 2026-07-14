from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pytest



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(15)
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")
    yield driver
    driver.quit()

def test_loading_images(driver):
    WebDriverWait(driver, 15).until(
    lambda d: len(d.find_elements(By.CSS_SELECTOR, "#image-container img[src]")) == 4
)

    # Шаг 3: берём третье изображение (индекс 2)
    images = driver.find_elements(By.TAG_NAME, "img")
    third_image = driver.find_element(By.ID, "award")

    # Шаг 4: читаем атрибут alt и проверяем
    alt_value = third_image.get_attribute("alt")
    assert alt_value == "award", f"Ожидали 'award', получили '{alt_value}'"