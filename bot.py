from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from fake_useragent import UserAgent
import time

from secret import login, password


def login_n_authorisation():
    url = "https://polezniemelochi.ru/user/auth/"

    options = webdriver.ChromeOptions()

    options.add_argument("start-maximized")
    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    # url = f'{first}{second}' if second is not None else f'{first}'
    try:
        driver.get(url=url)
        time.sleep(5)

        email_input = driver.find_element('name', "mail")
        email_input.clear()
        email_input.send_keys(login)
        time.sleep(1)

        password_input = driver.find_element('name', "password")
        password_input.clear()
        password_input.send_keys(password)

        press = driver.find_element('xpath', '''//*[@id="content"]/div[1]/div/main/div[2]/form/div[5]/input''')
        press.click()
        time.sleep(5)

        return driver

    except Exception as ex:
        print(ex)
        driver.close()
        driver.quit()
# html = driver.page_source

