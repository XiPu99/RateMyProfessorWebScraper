from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
import time, bs4


#====================================================================================
#  Using Selenium to keep clicking load more button to get a full list of professors
#====================================================================================

# a function that check whether an element exist on current page based on the css selector passed in
def checkIfExist(driver, cssSelector):
    try:
        driver.find_element_by_css_selector(cssSelector)
    except NoSuchElementException:
        return False
    return True

# check if an element has a style attribute that sets its display to none or not
def checkIfDisplay(element):
    return element.get_attribute('style')!='display: none;'

# open google chrome with a custom profile instead of a default temporary profile
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/Users/xipu/Library/Application Support/Google/Chrome/Default")
driver = webdriver.Chrome('/Users/xipu/Desktop/PythonScripts/chromedriver', chrome_options=options)
driver.minimize_window()

# go to ratemyprofessors page for Duke(you can always change the link below into your own school's)
driver.get('http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Barnard+College&schoolID=83&queryoption=TEACHER')

# get the load more button
wait = WebDriverWait(driver, 5)
loadMore = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#mainContent .result-list .progressbtnwrap')
        )
    )

# keep clicking load more button until we reach the end of the list
while checkIfDisplay(loadMore):
    driver.execute_script("document.querySelector('#mainContent .result-list .content').click()")


#====================================================
#  Using BeautifulSoup to scrape data from the page
#====================================================

# get page's html source code
html = driver.page_source
soup = bs4.BeautifulSoup(html, 'html.parser')
counter = 0 # create a variable to keep track of how many professors are there on the page

# print table's header
print('======================================================')
print('{0:10}{1:25}{2:3}'.format('ID', 'NAME', 'RATING'))

# loop through each professor and print data
for prof in soup.select('#mainContent .result-list li'):

    rating = prof.find('span', class_='rating').text
    if(rating=='N/A'): break
    info = prof.find('span', class_='name')
    id = prof.find('span', class_='remove-this-button')
    # link = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid={0}&showMyProfs=true'.format(id['data-id'])
    # print(link)
    print('{0:10}{1:25}{2:3}'.format(id['data-id'], info.contents[0].strip(), rating))
    counter += 1

print('There are ' + str(counter) + ' professors in total with at least one rating')
print('======================================================')
# close the browser
driver.quit()
