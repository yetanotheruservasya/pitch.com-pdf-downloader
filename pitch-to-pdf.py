from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image
from io import BytesIO

from tqdm import tqdm
import time
import sys

# Selenium settings to disable logs and run headless
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')


# Args from console
if len(sys.argv) == 1:
    raise Exception('Missing url parameter')
url = sys.argv[1]
if len(sys.argv) > 2:
    resolution = sys.argv[2]
else:
    resolution = '4K'

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

# Loading page, wait 1s for page to load
driver = webdriver.Chrome(options = chrome_options)
driver.get(url)
time.sleep(2)

# Finding number of slides and the button for the next slide
n_slides = len(driver.find_elements(By.CLASS_NAME, 'dash'))
next_btn = driver.find_elements(By.CLASS_NAME, 'player-v2--button')[1]

# Taking a screenshot of all slides
png_slides = []
print('\nScraping slides from pitch.com...')
for n in tqdm(range(n_slides)):
    slide = driver.find_element(By.CLASS_NAME, 'slide-wrapper')
    png_slides.append(slide.screenshot_as_png)
    if n < n_slides - 1:
        next_btn.click()
print('Slides scraped!')

# Loading from memory and converting RGBA to RGB
def foo(png):
    img = Image.open(BytesIO(png))
    img.load()
    background = Image.new('RGB', img.size, (255, 255, 255))
    background.paste(img, mask = img.split()[3])
    return background

# Saving the screenshots as a PDF using Pillow
print('\nConverting RGBA to RGB...')
images = [foo(png) for png in tqdm(png_slides)]
print('Conversion finished!')

output_name = driver.title + '.pdf'
print('\nSaving deck as "' + output_name + '"...')
images[0].save(
    output_name, "PDF", resolution = 100.0, save_all = True, append_images = images[1:]
)
print('Deck saved!')