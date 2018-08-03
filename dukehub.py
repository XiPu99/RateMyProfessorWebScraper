from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import time, bs4

driver.get('https://my.duke.edu/students/')
driver.minimize_window()
food = driver.find_element_by_partial_link_text("Food/Flex Accounts")
food.click()

driver.find_element_by_id('j_username').send_keys('xp19')
driver.find_element_by_id('j_password').send_keys('Xp99*801')
driver.find_element_by_id('Submit').click()

try:
    flex = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#container tr:nth-of-type(1) td'))
        )
    food = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#container tr:nth-of-type(2) td'))
        )
    print('Your flex amount is ' + flex.get_attribute('innerHTML'))
    print('Your food amount is ' + food.get_attribute('innerHTML'))

finally:
    driver.quit()

# unsuccessful attempt in logging in without using web driver
# s = requests.session()
# login = s.get('https://authentication.oit.duke.edu')
# login.raise_for_status()
#
# login_html = bs4.BeautifulSoup(login.text, 'html.parser')
# print(login_html.title)
# hidden_inputs = login_html.select('input[type=hidden]')
# for x in hidden_inputs:
#     print(x.get('value'))
#
# payload = { 'j_username': 'xp19',
#             'j_password': 'Xp99*801',
#             'loginPageTime': '1532916758061',
#             'submit': ''}
