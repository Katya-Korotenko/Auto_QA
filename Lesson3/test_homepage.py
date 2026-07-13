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
    driver.get("https://itcareerhub.de/ru")
    yield driver
    driver.quit()


ELEMENTS = [
    ("Логотип ITCareerHub",     By.CSS_SELECTOR,   "img[alt='IT Career Hub']"),
    ("Ссылка Программы",         By.LINK_TEXT,       "Программы"),
    ("Ссылка Способы оплаты",    By.LINK_TEXT,       "Способы оплаты"),
    ("Ссылка О нас",             By.LINK_TEXT,       "О нас"),
    ("Ссылка Отзывы",            By.LINK_TEXT,       "Отзывы"),
    ("Ссылка Блог",              By.LINK_TEXT,       "Блог"),
    ("Кнопка языка RU",          By.CSS_SELECTOR, "a[href='/ru']"),
    ("Кнопка языка DE",          By.LINK_TEXT, "de"),
]


@pytest.mark.parametrize("by, locator", ELEMENTS, ids=[e[0] for e in ELEMENTS])
def test_element_is_displayed(driver, name, by, locator):
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((by, locator))
    )
    assert element.is_displayed()



SUB_MENU_ABOUT = [(By.LINK_TEXT, "О компании"),
             ( By.LINK_TEXT, "Контакты"),
             ( By.LINK_TEXT, 'Работа у нас')]

@pytest.mark.parametrize("by, locator", SUB_MENU_ABOUT, ids=[e[1] for e in SUB_MENU_ABOUT])
def test_about_submenu_is_displayed(driver, by, locator):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "О нас"))
    ).click()
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((by, locator))
    )
    assert element.is_displayed()



# задания 3,4,5
def test_button_call(driver):

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "О нас"))
    ).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Контакты"))
    ).click()

    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'ОБРАТНЫЙ ЗВОНОК'))
    )

    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
    try:
        button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", button)

    popup = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-tooltip-hook='#popup:form-tr']"))
    )
    assert popup.is_displayed()

    heading = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[field='tn_text_175871291756015470']"))
    )
    assert "карьерную консультацию" in heading.text


# доп тест
SUB_PROGRAMS = [("Ссылка Аналитик данных +AI", By.LINK_TEXT, "Аналитик данных +AI"),
             ("Ссылка UX/UI дизайнер +AI", By.LINK_TEXT, 'UX/UI дизайнер +AI'),
             ("Ссылка Специалист по AI-автоматизации ", By.LINK_TEXT, 'Специалист по AI-автоматизации'),
             ("Ссылка Python-разработчик + AI", By.LINK_TEXT, 'Python-разработчик + AI'),
             ("Ссылка Веб-разработчик + AI", By.LINK_TEXT, 'Веб-разработчик + AI'),]


@pytest.mark.parametrize("name, by, locator", SUB_PROGRAMS, ids=[e[0] for e in SUB_PROGRAMS])
def test_sub_menu_is_displayed(driver, name, by, locator):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Программы"))
    ).click()
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((by, locator))
    )
    assert element.is_displayed(), f"{name} не отображается на странице"