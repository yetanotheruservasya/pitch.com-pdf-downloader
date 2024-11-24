import os
from flask import Flask, request, jsonify, send_file
from utils.slide_downloader import SlideDownloader
import ocrmypdf

app = Flask(__name__)

# Путь для хранения скачанных файлов
downloads_dir = os.path.join(os.getcwd(), 'decks')
os.makedirs(downloads_dir, exist_ok=True)

@app.route('/download', methods=['POST'])
def download_slides():
    data = request.get_json()

    # Проверка, что в запросе есть URL
    if 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    url = data['url']
    resolution = data.get('resolution', 'HD')
    skip_ocr = data.get('skip_ocr', True)
    
    # Скачивание слайдов
    try:
        sd = SlideDownloader(resolution)
        pdf_path = sd.download(url)

        # Если OCR не отключен, запускаем его
        if not skip_ocr and pdf_path:
            print('\nRunning OCR... (disable with the flag --skip-ocr)')
            ocrmypdf.ocr(pdf_path, pdf_path, deskew=True)
            print('OCR finished!')

        # Получаем оригинальное имя файла для сохранения
        filename = os.path.basename(pdf_path)
        
        # Отправляем файл на скачивание с правильным именем
        if os.path.exists(pdf_path):
            response = send_file(pdf_path, as_attachment=True, download_name=filename)
            return response
        else:
            return jsonify({'error': f'File not created: {pdf_path}'}), 500

    except Exception as e:
        return jsonify({'error': f'Failed to process document: {str(e)}'}), 500
    
    finally:
        # Очистка, если файл существует
        if os.path.exists(pdf_path):
            try:
                os.remove(pdf_path)
                print(f"File {pdf_path} deleted successfully")
            except Exception as e:
                app.logger.error(f'Failed to delete the file {pdf_path}: {str(e)}')

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    try:
        # Очистка всех файлов в каталоге decks
        for filename in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File {filename} deleted successfully")
        
        return jsonify({'message': 'All files cleaned up successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to clean up files: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
