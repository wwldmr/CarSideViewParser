import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By

def download_image(url, filename):
    if url.startswith('data:image/'):
        # Изображение в кодировке Base64
        print(f"Skipping base64Сoded image: {url}")
        return
    else:
        # Обычный URL изображения
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)

def search_and_download(query, num_images):
    driver = webdriver.Firefox()
    driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

    images = driver.find_elements(By.XPATH, '//img[contains(@class,"rg_i")]')

    for i, img in enumerate(images[:num_images]):
        image_url = img.get_attribute('src')
        download_image(image_url, f"C:/projects/CarSideViewParser/downloads/{query}_{i}.jpg")

search_query = input("Что: ")
num_images_to_download = int(input("Сколько: "))

search_and_download(search_query, num_images_to_download)