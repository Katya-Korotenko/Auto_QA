
import pytest, time, math
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import os

@pytest.fixture()
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

def test_with_tabs(driver):
    # sleep(3)
    driver.get("https://the-internet.herokuapp.com/javascript_alerts")
    driver.execute_script("window.open('https://the-internet.herokuapp.com/javascript_alerts', '_blank');")
    driver.execute_script("window.open('https://google.com', '_blank');")
    # Получаем список всех вкладок
    tabs = driver.window_handles
    print("Идентификаторы вкладок:", tabs)
    # Переключаемся на вторую вкладку (Google)
    sleep(2)
    driver.switch_to.window(tabs[0])
    sleep(2)
    print("Текущая вкладка:", driver.current_window_handle)
    driver.close()
    sleep(2)
    tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    print("Текущая вкладка:", driver.current_window_handle)
    sleep(2)