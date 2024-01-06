import sys
from utils.slide_downloader import SlideDownloader

if __name__ == '__main__':


    # Args from console
    if len(sys.argv) == 1:
        raise Exception('Missing url parameter')
    url = sys.argv[1]
    if len(sys.argv) > 2:
        resolution = sys.argv[2]
    else:
        resolution = '4K'

    sd = SlideDownloader(resolution)

    pdf_path = sd.download(url)

    # testing: https://pitch.com/public/babe4b9d-f535-4b8d-b206-c12af886bdb0


    
