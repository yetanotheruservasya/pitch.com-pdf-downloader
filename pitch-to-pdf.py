# TODO:
# hubspot
# box.com
# google drive : https://sites.google.com/a/gooapps.edu.vn/app-learning-center/tips-library/docs-tips/prevent-others-from-downloading-printing-and-copying-shared-drive-files
# others ... ?


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
# chrome_options.add_argument('--headless')
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
time.sleep(5)

# Taking a screenshot of all slides
def scrape_slides(n_slides, next_btn, find_slide_fun, find_slide_params):

    png_slides = []
    print('\nScraping slides...')
    for n in tqdm(range(n_slides)):
        slide = find_slide_fun(*find_slide_params)
        png_slides.append(slide.screenshot_as_png)
        if n < n_slides - 1:
            # Use JS in case it's hidden
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(1.5)
    print('Slides scraped!')
    return png_slides


if 'pitch.com' in url:

    # Cookie accept - do not accept tracking
    btn = driver.find_elements(By.XPATH, '//button[@type="text"]')
    if len(btn) > 0:
        btn = btn[0]
        btn.click()
        time.sleep(1)
        no_tracking = driver.find_elements(By.XPATH, '//input[@name="engagement"]')[0]
        no_tracking.click()
        time.sleep(1)
        confirm = driver.find_elements(By.XPATH, '//button[@type="submit"]')[0]
        confirm.click()
        time.sleep(1)

    n_slides = len(driver.find_elements(By.CLASS_NAME, 'dash'))
    next_btn = driver.find_elements(By.CLASS_NAME, 'ng-player-v2--button')[1]
    png_slides = scrape_slides(n_slides, next_btn, driver.find_element, (By.CLASS_NAME, 'slide-wrapper'))

elif 'canva.com' in url:
    
    # Accept cookies
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for b in buttons:
        if 'Accept' in b.text:
            b.click()
            time.sleep(1)
            break

    n_slides = driver.find_elements(By.XPATH, '//*[@aria-valuemax]')[0].get_property('ariaValueMax')
    n_slides = int(n_slides)

    # Hiding the footer & header (otherwise visible in slide)
    footer = driver.find_elements(By.TAG_NAME, 'footer')[0]
    header = driver.find_elements(By.TAG_NAME, 'header')[0]
    driver.execute_script("arguments[0].style.opacity = 0;", footer)
    driver.execute_script("arguments[0].style.opacity = 0;", header)

    next_btn = driver.find_elements(By.TAG_NAME, 'button')[4]
    if '/' in next_btn.text:
        next_btn = driver.find_elements(By.TAG_NAME, 'button')[5]
    if next_btn.text != '':
        print('Found wrong next button...')
        print(next_btn.text)
        raise Exception('Wrong next button!')
    
    png_slides = scrape_slides(n_slides, next_btn, driver.find_element, (By.XPATH, '//*[contains(@style, "translate")]'))


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