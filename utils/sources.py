from selenium.webdriver.common.by import By
import time

def get_canva_params(driver):
    '''
    Preprocesses Canva and returns params to find all slides
    '''

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
    
    params = dict(
        n_slides = n_slides,
        next_btn = next_btn,
        slide_selector = (By.XPATH, '//*[contains(@style, "translate")]')
    )

    return params


def get_pitch_params(driver):
    '''
    Preprocesses Pitch.com and returns params to find all slides
    '''

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
    
    # Deleting the popup shown at the end of the presentation
    try:
        driver.execute_script("document.getElementsByClassName('player-branding-popover')[0].remove();")
    except Exception:
        print('Could not remove branding popover...')

    n_slides = len(driver.find_elements(By.CLASS_NAME, 'dash'))

    # Named differently at times?
    btns = driver.find_elements(By.CLASS_NAME, 'ng-player-v2--button')
    if len(btns) == 0:
        btns = driver.find_elements(By.CLASS_NAME, 'player-v2--button')
    next_btn = btns[1]

    params = dict(
        n_slides = n_slides,
        next_btn = next_btn,
        slide_selector = (By.CLASS_NAME, 'slide-wrapper')
    )

    return params

# Check if we're at the end of the current slide (gradually adding elements)
def pitch_at_slide_end(driver):

    current_dash = driver.find_element(By.CSS_SELECTOR, '.dash.selected [aria-valuenow]')

    aria_valuenow = current_dash.get_attribute('aria-valuenow')

    return aria_valuenow == '100'

