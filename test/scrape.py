# Imports
import os
import sys
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Get project root directory
try:
    project_root = os.path.dirname(os.path.realpath(__file__))
except: # If running from an IDE
    project_root = os.getcwd()
# append path
sys.path.append(project_root)

#### Setup Logging

# Ensure log directory exists
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)

# Setup logging to write instead of append
log_file = os.path.join(log_dir, 'scrape.log')
logging.basicConfig(filename=log_file, filemode='w', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Optionally, add console handler for debugging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)

# Optionally, create a named logger
logger = logging.getLogger('scrape.py')

















# Setup selenium
logger.info('Setting up selenium')

# Driver path
driver_path = r"C:\Users\tuan\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
logger.info(f'Driver path: {driver_path}')
# Service, options, driver
service = Service(executable_path=driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


# Login
url = 'https://www.volosports.com/login'
logger.info(f'Navigating to {url}')
driver.get(url)
# Enter username: <input id="credential" type = "text"
username = 'donaldinho'
password = 'onetwo34'
logger.info(f'Entering username: {username}')
user_element = driver.find_element(By.ID,'credential')
user_element.send_keys(username)
# Enter password: <input id="password" type = "password"
logger.info(f'Entering password')
pass_element = driver.find_element(By.ID,'password')
pass_element.send_keys(password)
# pass_element: Hit enter key
logger.info('Logging in...')
pass_element.submit()

# Naviagate to registration
url_login = 'https://www.volosports.com/app/register/6603018eff3253704e05f6c8/rtype'
logger.info(f'Navigating to {url_login}')
driver.get(url_login)

# Click on register button
# <a type="button" class="button_button__zpxkc w-100 main_primary-btn__1xCld" href="/app/register/6603018eff3253704e05f6c8/rtype">Register</a>
logger.info('Clicking on register button...')
register_button = driver.find_element(By.XPATH, '//a[@href="/app/register/6603018eff3253704e05f6c8/rtype"]')
register_button.click()


# Test codes
arr_codes = ['TEST10','TEST20','volosmith','TEST30','TEST40','TEST50','TEST60','TEST70','TEST80','TEST90','TEST100']
# Read fuzzy coupons text
fp_txt = r"C:\Users\tuan\Downloads\FuzzCoupons-master\FuzzCoupons-master\fuzzcoupons.txt"
with open(fp_txt, 'r') as f:
    arr_codes = f.read().split('\n')
len(arr_codes)
# Find position of code 50off1912
arr_codes.index('50off1912')

sleep_1 = 1
sleep_2 = 1
# Loop through test codes
dict_codes = {} # code: total
for code in arr_codes[1521:]:
    # Click enter promo code
    # <a class="main_underline__Z4+Ky col-7 p-0 text-right" role="button" tabindex="0">Enter Code</a>
    logger.info('Clicking on enter promo code button...')
    promo_button = driver.find_element(By.XPATH, '//a[@role="button"]')
    promo_button.click()

    # Click on promo code input
    # <input class="fancy_fancyField__Bdnxm w-100 fancy_blockStyle__sWtFn" type="text" autocomplete="" placeholder="Enter promo" value="" style="width: 40%;">
    promo_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter promo"]')

    logger.info(f'Entering promo code: {code}')
    promo_input.send_keys(code)
    logger.info(f'Sleeping for {sleep_1} seconds...')
    time.sleep(sleep_1)
    # Send enter key
    logger.info('Submitting promo code...')
    # Click apply button
    # <a class="main_apply-button__hVNHr" role="button" tabindex="0">Apply</a>
    apply_button = driver.find_element(By.XPATH, '//a[@role="button"]')
    apply_button.click()
    # Sleep for 5 seconds
    logger.info(f'Sleeping for {sleep_2} seconds...')
    time.sleep(sleep_2)
    # Get order total reading
    # <div class="d-flex align-items-center justify-content-between mb-4 mt-3"><p class="font-weight-bold">Order Total </p><p class="mb-0 font-weight-bold"><span><span>$79.28</span></span></p></div>
    order_total = driver.find_element(By.XPATH, '//div[@class="d-flex align-items-center justify-content-between mb-4 mt-3"]')
    logger.info(f'Order total: {order_total.text}')
    # 'Order Total\n$79.28' Remove 'Order Total\n'
    order_total = order_total.text.split('\n')[1]
    # Remove '$' and convert to float
    order_total = float(order_total[1:])
    # Compare to base 79.28
    discount = round(79.28 - order_total,2)
    if discount > 1:
        logger.info(f'Code: {code}, Discount: {discount}')
        dict_codes[code] = discount
    print("Current discount list: ", dict_codes)
    
logger.info(f'Promo codes: {dict_codes}')

df = pd.DataFrame(dict_codes.items(), columns=['Code','Discount'])
df.to_excel('volo bruteforced discounts.xlsx',index=False)
os.startfile('volo bruteforced discounts.xlsx')