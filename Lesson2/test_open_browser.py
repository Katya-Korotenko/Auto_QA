from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pytest
# import os


@pytest.fixture
def driver():
    # service = Service("/Users/romansurkov/Documents/chromedriver-mac-arm64/chromedriver")
    # options = Options()
    # driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Chrome()
    driver.maximize_window()
    # driver.set_window_size(640, 460)
    # driver = webdriver.Chrome(service=service)
    # driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_about_page(driver):
    driver.get("https://itcareerhub.de/ru")
    sleep(3)
    about_link = driver.find_element(By.LINK_TEXT, "О нас")
    about_link.click()
    sleep(3)

def test_berlin(driver):
    driver.get("https://itcareerhub.de/ru")
    driver.refresh()
    driver.get("https://www.berlin.de")
    driver.save_screenshot("./berlin_ds.png")
    sleep(2)
    driver.refresh()
    driver.back()
    # sleep(2)
    driver.forward()
    driver.refresh()
    # sleep(2)