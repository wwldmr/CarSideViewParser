import os
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException


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


def load_page(driver):
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
            try:
                # click on show more button (in my query is one on page)
                driver.find_element(By.CLASS_NAME, "LZ4I").click()
            except ElementNotInteractableException as e:
                print(e)
        last_height = new_height


def scroll_to_top(driver):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)


def search_and_download(query, num_images):
    # creates a directory where photos will be uploaded
    if not os.path.exists(f'downloads/{query}'):
        os.makedirs(f'downloads/{query}')

    # use your browser if you need this
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/search?q={query}&source=lnms&tbm=isch")

    # there was a need to remove the header
    # because it did not allow to click on the button
    # that closes the additional page on the left
    # on this cause additional page is not visible
    delete_header(driver)

    # preload page for the driver to find all the pics
    load_page(driver)
    # scroll_to_top(driver)

    time.sleep(1000)

    images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')

    # for i, img in enumerate(images[:num_images]):
    #     try:
    #         try:
    #             img.click()
    #         except ElementNotInteractableException as e:
    #             print(img, e)
    #             continue
    #         image_src = WebDriverWait(driver, 4).until(
    #             EC.presence_of_element_located((By.CLASS_NAME, 'iPVvYb'))
    #         ).get_attribute('src')
    #         try:
    #             download_image(image_src, f"./downloads/{query}/{query}_{i}.jpg")    # os.path.basename(image_src)
    #         except Exception as e:
    #             print("Probably base64 encoded pic ", e)
    #             continue
    #         # finds the close button on the additional page on the left
    #         driver.execute_script("document.querySelector('.uj1Jfd').click();")
    #     except TimeoutException as e:
    #         print(e)
    #         driver.execute_script("document.querySelector('.uj1Jfd').click();")
    #         continue
    #
    # driver.quit()


search_query = "car side view"
num_of_images = 1000

search_and_download(search_query, num_of_images)
