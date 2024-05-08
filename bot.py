from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Keys

import time
import json
import os

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


def click_(cat_name, web_driver, category_url=None, tag_name='div'):
    try:
        if category_url:
            driver.get(url=category_url)
            time.sleep(4)

        category_list = web_driver.find_elements(By.CLASS_NAME, 'name')

        for category in category_list:
            if category.tag_name == tag_name:
                if category.text == cat_name:
                    category.click()
                    time.sleep(2)

                    return web_driver.current_url

    except Exception as E:
        web_driver.close()
        web_driver.quit()
        print(E)


def product_edit(web_driver, product, subcategory_url):
    if driver.current_url != subcategory_url:
        check_availability = click_(product, web_driver, subcategory_url, tag_name='span')
    else:
        check_availability = click_(product, web_driver, tag_name='span')

    if not check_availability:
        return 'Товар не найден!'

    edit = web_driver.find_element('xpath', '''//*[@id="admin_menu"]/ul/li[2]/ul/li[5]/a''')
    edit.click()

    time.sleep(2)

    fraction_field = web_driver.find_element(By.NAME, 'a-381')
    fraction_field.clear()
    fraction_field.send_keys('0.1')

    fraction_field.send_keys(Keys.ENTER)
    time.sleep(1)


if __name__ == "__main__":
    directory = r'C:\Users\Administrator\fractionalsale'

    file_list = [filename for filename in os.listdir(directory) if os.path.isfile(os.path.join(directory, filename))]
    json_list = [file for file in file_list if file.split('.')[-1] == 'json']

    if json_list:
        driver = login_n_authorisation()

        for json_file in json_list:
            with open(json_file, 'r') as file:
                data_dict = json.load(file)

            category_name = json_file.replace('.json', '')
            main_category_url = click_(category_name, driver)

            for data_key, data_list in data_dict.items():
                if data_key == 'Гвозди':
                    continue

                if data_list:
                    subcategory_url = click_(data_key, driver, main_category_url)
                    for product in data_list:
                        status = product_edit(web_driver=driver, product=product, subcategory_url=subcategory_url)
                        if status == 'Товар не найден!':
                            continue

