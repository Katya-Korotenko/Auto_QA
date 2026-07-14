from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest
import time



@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://bonigarcia.dev/selenium-webdriver-java/iframes.html")
    yield driver
    driver.quit()


def test_iframe(driver):
    target_text = "semper posuere integer et senectus justo curabitur."
    iframe = driver.find_element(By.ID, "my-iframe")
    driver.switch_to.frame(iframe)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "content"))
    )

    assert target_text in element.text
    assert element.is_displayed()

    # Подсветка блока — только если параграф нашёлся
    for p in element.find_elements(By.TAG_NAME, "p"):
        if target_text in p.text:
            driver.execute_script("""
                arguments[0].style.backgroundColor = 'yellow';
                arguments[0].style.border = '2px solid red';
            """, p)
            break
