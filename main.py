import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from bs4 import BeautifulSoup

chromePath = r'/home/cujomo/chromedriver'

wd = webdriver.Chrome(executable_path= chromePath)
loginUrl = 'https://www.linkedin.com'

def login(email,password):
    wd.get(loginUrl)

    email_input = wd.find_element_by_class_name('login-email')
    password_input = wd.find_element_by_class_name('login-password')

    email_input.send_keys('email')
    password_input.send_keys('password')

    password_input.send_keys(Keys.ENTER)

    cookies = wd.get_cookies()

    for cookie in cookies:
        wd.add_cookie(cookie)

    wd.get('https://www.linkedin.com/in/austinoboyle/')

def scroll_to_bottom():
    #Scroll to the bottom of the page
    expandable_button_selectors = [
        'button[aria-expanded="false"].pv-skills-section__additional-skills',
        'button[aria-expanded="false"].pv-profile-section__see-more-inline',
        'button[aria-expanded="false"].pv-top-card-section__summary-toggle-button',
        'button[data-control-name="contact_see_more"]'
    ]
    current_height = 0
    while True:
        for name in expandable_button_selectors:
            try:
                wd.find_element_by_css_selector(name).click()
            except:
                pass
        # Scroll down to bottom
        new_height = wd.execute_script(
            "return Math.min({}, document.body.scrollHeight)".format(current_height + 280))
        if (new_height == current_height):
            break
        wd.execute_script(
            "window.scrollTo(0, Math.min({}, document.body.scrollHeight));".format(new_height))
        current_height = new_height
        # Wait to load page
        time.sleep(0.4)

def open_more():
    eles= wd.find_elements_by_css_selector('.lt-line-clamp__more')
    for ele in eles:
        try:
            wd.execute_script('arguments[0].disabled = true;',ele)
            wd.execute_script('arguments[0].click();',ele)
        except:
            pass