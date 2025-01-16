"""
Скрипт для загрузки презентаций с сайтов pitch.com и canva.com и сохранения их в формате PDF.
"""

import argparse
from utils.slide_downloader import SlideDownloader

if __name__ == '__main__':

    # Parsing input args
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help = 'The url to download the slides from')
    parser.add_argument(
        '-r',
        '--resolution',
        default = 'HD'
    )
    parser.add_argument(
        '--skip-ocr',
        action = 'store_true',
        dest = 'skip_ocr',
        help = 'Disable OCR'
    )
    args = parser.parse_args()

    # Saving the presentation as a PDF
    sd = SlideDownloader(args.resolution)
    PDF_PATH = sd.download(args.url)

    # Running ocr.
    if not args.skip_ocr:
        print('\nRunning OCR... (disable with the flag --skip-ocr)')
        import ocrmypdf
        ocrmypdf.ocr(PDF_PATH, PDF_PATH, deskew = True)
        print('OCR finished!')
