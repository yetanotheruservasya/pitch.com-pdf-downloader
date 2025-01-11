import requests

# Адрес вашего сервиса
BASE_URL = "http://127.0.0.1:5000"

# Скачивание слайдов
download_data = {
    "url": "https://pitch.com/v/the-neural-interface-weve-all-been-waiting-for-vk38b8",
    "resolution": "HD",
    "skip_ocr": True
}

response = requests.post(f"{BASE_URL}/download", json=download_data)

if response.status_code == 200:
    with open("downloaded_slide.pdf", "wb") as file:
        file.write(response.content)
    print("Файл успешно скачан и сохранен как 'downloaded_slide.pdf'")
else:
    print(f"Ошибка: {response.json()}")

# Очистка файлов
cleanup_response = requests.post(f"{BASE_URL}/cleanup")
if cleanup_response.status_code == 200:
    print("Очистка файлов выполнена успешно")
else:
    print(f"Ошибка очистки: {cleanup_response.json()}")
