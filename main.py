import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def download_image(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        file.write(response.content)


def search_and_download(query, num_images):
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    driver = webdriver.Firefox()
    driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

    images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')

    for i, img in enumerate(images):
        img.click()
        time.sleep(2)
        image_url = driver.find_element(By.CLASS_NAME, 'iPVvYb').get_attribute('src')
        if image_url.startswith('data:image/'):
            continue
        download_image(image_url, f"./downloads/{query}_{i}.jpg")
        driver.find_element(By.CSS_SELECTOR, '[aria-label="Закрыть"]').click()
    driver.quit()


search_query = input("Что: ")
num_images_to_download = int(input("Сколько: "))

search_and_download(search_query, num_images_to_download)