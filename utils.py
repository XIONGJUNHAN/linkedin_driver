def func1(a,b):
    return a+b
    
def func2(a,b):
    return a-b

import bs4
import logging
from metadrive._selenium import get_driver

driver = get_driver()
driver.get('http://www.example.com/')

# DRIVER EXAMPLE
link_clicked = None
try:
    link = driver.find_element_by_partial_link_text('ore information')
    link.click()
    link_clicked = True
except:
    link_clicked = False
    logging.warning('could not click')

# SOUP EXAMPLE
soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')

test_link = soup.find('a', {'class': 'test'})
test_link.text

if test_link is not None:
    result = {'url': test_link.attrs['href'],
              'name': test_link.text}
else:
    result = {}
    raise Exception("Could not find the URL about example.")