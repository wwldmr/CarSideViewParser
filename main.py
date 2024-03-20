from bs4 import BeautifulSoup
import requests
import shutil

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
    url = "https://www.google.com/search"
    params = {
        "q": query,
        "tbm": "isch",
        "ijn": "0"
    }
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        image_tags = soup.select('img.rg_i')
        # print(soup.find_all('img', class_='rg_i'))
        # print(f"{soup.select('img.rg_i')}")
        for i, image_tag in enumerate(image_tags[:num_images]):
            image_url = image_tag['src']
            download_image(image_url, f"C:/projects/CarSideViewParser/downloads/{query}_{i}.jpg")
    else:
        print("Error:", response.status_code)

search_query = input("Что: ")
num_images_to_download = int(input("Сколько: "))

search_and_download(search_query, num_images_to_download)