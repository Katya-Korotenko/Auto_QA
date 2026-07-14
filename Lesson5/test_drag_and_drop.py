from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest




@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://www.globalsqa.com/demo-site/draganddrop/")
    yield driver
    driver.quit()


def test_drag_and_drop(driver):
    # закрываем куки если есть
    try:
        cookie_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-cta-consent"))
        )
        cookie_btn.click()
    except:
        pass

    iframe = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame"))
    )
    driver.switch_to.frame(iframe)


    first_photo = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#gallery li"))
    )
    trash = driver.find_element(By.ID, "trash")

    # source и target
    ActionChains(driver).drag_and_drop(first_photo, trash).perform()

    # Ждём пока в корзине появится 1 элемент
    WebDriverWait(driver, 10).until(
        lambda d: len(trash.find_elements(By.CSS_SELECTOR, "li")) == 1
    )

    # Ждём пока в галерее останется 3 элемента
    WebDriverWait(driver, 10).until(
        lambda d: len(d.find_elements(By.CSS_SELECTOR, "#gallery li")) == 3
    )


    assert len(trash.find_elements(By.CSS_SELECTOR, "li")) == 1
    assert len(driver.find_elements(By.CSS_SELECTOR, "#gallery li")) == 3