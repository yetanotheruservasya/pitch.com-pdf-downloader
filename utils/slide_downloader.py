from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from PIL import Image
from io import BytesIO

from tqdm import tqdm
import time

from utils import sources


class SlideDownloader:

    def __init__(self, resolution):

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--log-level=3')

        # Setting resolution
        if resolution == 'HD':
            res = 'window-size=1920,1080'
        elif resolution == '4K':
            res = 'window-size=3840,2160'
        elif resolution == '8K':
            res = 'window-size=7680,4320'
        else:
            raise Exception('Only HD, 4K and 8K resolutions allowed!')
        chrome_options.add_argument(res)

        # Initializing the driver
        self.driver = webdriver.Chrome(options = chrome_options)
    

    def _scrape_slides(self, n_slides, next_btn, slide_selector):
        '''
        Takes a screenshot of all slides and returns a list of pngs

        n_slides: int, the number of slides
        next_btn: clickable element on website to go to the next slide
        slide_selector: arguments to driver.find_element to locate the slide e.g. (By.XPATH, xpath_string)
        '''

        png_slides = []
        print('\nScraping slides...')
        for n in tqdm(range(n_slides)):
            slide = self.driver.find_element(*slide_selector)
            png_slides.append(slide.screenshot_as_png)
            if n < n_slides - 1:
                # Use JS in case it's hidden
                self.driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(1.5)
        print('Slides scraped!')
        return png_slides
    
    def download(self, url):
        '''
        Given an URL, loops over slides to screenshot them and saves a PDF
        '''

        url = url.lower()

        self.driver.get(url)
        time.sleep(5)

        if 'pitch.com' in url:
            params = sources.get_pitch_params(self.driver)
        elif 'canva.com' in url:
            params = sources.get_canva_params(self.driver)
        else:
            raise Exception('URL not supported...')
        
        png_slides = self._scrape_slides(params['n_slides'], params['next_btn'], params['slide_selector'])

        # Helper: Loading from memory and converting RGBA to RGB
        def _rgba_to_rgb(png):
            img = Image.open(BytesIO(png))
            img.load()
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask = img.split()[3])
            return background

        # Saving the screenshots as a PDF using Pillow
        print('\nConverting RGBA to RGB...')
        images = [_rgba_to_rgb(png) for png in tqdm(png_slides)]
        print('Conversion finished!')

        output_path = 'decks/' + self.driver.title + '.pdf'

        print('\nSaving deck as "' + output_path + '"...')
        images[0].save(
            output_path, "PDF", resolution = 100.0, save_all = True, append_images = images[1:]
        )
        print('Deck saved!')

        self.driver.close()

        return output_path









    