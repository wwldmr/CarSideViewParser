import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def download_image(url, filename):
    response = requests.get(url, stream=True).content
    with open(filename, 'wb') as file:
        file.write(response)


def delete_header(driver):
    script = """
    document.querySelector('.FA7L0b > div:nth-child(3)').remove();
    document.querySelector('.ndYZfc').remove();
    document.querySelector('#yDmH0d > c-wiz:nth-child(4)').remove();
    """
    driver.execute_script(script)
    time.sleep(1)


def scroll_to_bottom(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(1)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def scroll_to_top(driver):
    # Scroll up to upwards
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

def search_and_download(query, num_images):
    if not os.path.exists(f'downloads/{query}'):
        os.makedirs(f'downloads/{query}')

    driver = webdriver.Firefox()
    driver.get(f"https://www.google.com/search?q={query}&source=lnms&tbm=isch")

    delete_header(driver)
    scroll_to_bottom(driver)
    scroll_to_top(driver)

    images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')

    for i, img in enumerate(images[:num_images]):
        print(f"{img}\n")
        try:
            img.click()
            image_src = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'iPVvYb'))
            ).get_attribute('src')
            if image_src.startswith("data:image/"):
                continue
            download_image(image_src, f"./downloads/{query}/{query}_{i}.jpg")

            # Выполняет JavaScript код, который находит кнопку закрытия
            # selenium не справился (я тоже)
            driver.execute_script("document.querySelector('.uj1Jfd').click();")

        except Exception as e:
            print(e)
            driver.execute_script("document.querySelector('.uj1Jfd').click();")
            continue

    driver.quit()


search_query = input("Что: ")
num_images_to_download = int(input("Сколько: "))

search_and_download(search_query, num_images_to_download)