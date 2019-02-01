import re
import time

from metadrive._selenium import get_driver

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.common.action_chains import ActionChains

wd = get_driver()

email='3168095199@qq.com'
password = 'shelock007'


loginUrl = 'https://www.linkedin.com'

def login(email, password):
    wd.get(loginUrl)
    email_input = wd.find_element_by_class_name('login-email')
    password_input = wd.find_element_by_class_name('login-password')
    email_input.send_keys(email)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)

    # cookies = wd.get_cookies()
    #
    # for cookie in cookies:
    #     wd.add_cookie(cookie)

    #wd.get('https://www.linkedin.com/in/austinoboyle/')
    wd.get('https://www.linkedin.com/in/skhalifa/')

#must run the function in turns
def open_contact():
    '''needs to be called twice'''
    contact = wd.find_element_by_class_name('pv-top-card-v2-section__contact-info')
    wd.execute_script('arguments[0].disabled = true;',contact)
    wd.execute_script('arguments[0].click();',contact)

    contact_soup = BeautifulSoup(wd.page_source,'html.parser')
    career_card = contact_soup.find(class_ = 'ci-vanity-url')
    profile_url = [search['href'] for search in career_card.find_all('a')]
    website = contact_soup.find(class_ = 'ci-websites')
    web_url = [search['href'] for search in website.find_all('a')]
    web_type = [search.text.strip() for search in website.find_all('span')]
    websites = []
    for i in range(len(web_url)):
        websites.append({'type':web_type[i],'url':web_url[i]})
    contact = {"profile_url":profile_url,"websites":websites}
    print(contact)
    close = wd.find_element_by_class_name('artdeco-dismiss')
    ActionChains(wd).move_to_element(close).click().perform()
    

def scroll_to_bottom():
    #Scroll to the bottom of the page
    expandable_button_selectors = [
        'button[aria-expanded="false"].pv-top-card-section__summary-toggle-button',
        'button[aria-expanded="false"].pv-profile-section__see-more-inline',
        'button[aria-expanded="false"].pv-skills-section__additional-skills'
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
            "return Math.min({}, document.body.scrollHeight)".format(current_height + 300))
        if (new_height == current_height):
            break
        wd.execute_script(
            "window.scrollTo(0, Math.min({}, document.body.scrollHeight));".format(new_height))
        current_height = new_height
        # Wait to load page
        time.sleep(0.4)
        

def extract_interest(sou):
    box = []
    for item in sou.find_all('li',{'class' : 'entity-list-item'}):
        box.append({
            'img':item.find('img')['src'],
            'name':item.find('span',{'class':'pv-entity__summary-title-text'}).text,
            'number of followers':item.find('p',{'class':'pv-entity__follower-count'}).text.split(" ")[0]
        })
    return box


def open_interest():
    '''try it twice'''
    see_interest = wd.find_element_by_css_selector('a[data-control-name="view_interest_details"]')
    ActionChains(wd).move_to_element(see_interest).click().perform()
    
    interest_selector = ['a[data-control-name="following_companies"]','a[data-control-name="following_groups"]','a[data-control-name="following_schools"]'] 
    
    interests = []
    
    for name in interest_selector:
        try:
            wd.find_element_by_css_selector(name).click() 
            soup = BeautifulSoup(wd.page_source,'html.parser')
            interests.append(extract_interest(soup))
        except:
            pass
    print(interests)
    close = wd.find_element_by_class_name('artdeco-dismiss')
    '''WebDriverWait(wd,45).until(
        lambda x: x.find_element_by_class_name('artdeco-dismiss'))'''
    ActionChains(wd).move_to_element(close).click().perform()
    
        

def text_or_default_accomp(element, selector, default=None):
    try:
        s = element.select_one(selector).get_text().strip().split('\n')
        if len(s) == 2:
            return s[1].strip()
        else:
            return s[0].strip()
    except Exception as e:
        return default
    
    
def open_accompliments():
    
    soup0 = BeautifulSoup(wd.page_source,'html.parser')
    
    classification = []
        
    for cla in soup0.find_all('h3',{'class':'pv-accomplishments-block__title'}):
        classification.append(cla.text)
    
    accomp_expand = wd.find_elements_by_class_name('pv-accomplishments-block__expand')
    
    expand_box = soup0.find_all(class_ = 'pv-profile-section__see-more-inline')
    
    count = 0
    for btn in expand_box:
        if 'aria-controls' in btn.attrs:
            break
        count+=1

    
    content = []
    for accomp in accomp_expand:    
            ActionChains(wd).move_to_element(accomp).click().perform()
            expand_btn = wd.find_elements_by_class_name('pv-profile-section__see-more-inline')[count:]
            for btn in expand_btn:
                try:
                    ActionChains(wd).move_to_element(btn).click().perform()
                except:
                    pass
                
            soup = BeautifulSoup(wd.page_source,'html.parser') 

            class_block = soup.find_all('li',{'class':'pv-accomplishment-entity--expanded'})
            
            title = '.pv-accomplishment-entity__title'
            date = '.pv-accomplishment-entity__date'
            issuer = '.pv-accomplishment-entity__issuer'
            description = '.pv-accomplishment-entity__description'
            
            cont = []
            for item in class_block:
                cont.append({
                    'title':text_or_default_accomp(item,title),
                    'subtitle':{'date':text_or_default_accomp(item,date),'issuer':text_or_default_accomp(item,issuer)},
                   'description':text_or_default_accomp(item,description)  
                })
            
            content.append(cont)
            
            
    result = zip(classification,content)
    print(list(result))

def open_more():
    eles= wd.find_elements_by_css_selector('.lt-line-clamp__more')
    for ele in eles:
        try:
            wd.execute_script('arguments[0].disabled = true;',ele)
            wd.execute_script('arguments[0].click();',ele)
        except:
            pass
        

        
soup = BeautifulSoup(wd.page_source,'html.parser') 

def flatten_list(l):
    return [item for sublist in l for item in sublist]

def one_or_default(element, selector, default=None):
    """Return the first found element with a given css selector
    Params:
        - element {beautifulsoup element}: element to be searched
        - selector {str}: css selector to search for
        - default {any}: default return value
    Returns:
        beautifulsoup element if match is found, otherwise return the default
    """
    try:
        el = element.select_one(selector)
        if not el:
            return default
        return element.select_one(selector)
    except Exception as e:
        return default

def text_or_default(element, selector, default=None):
    """Same as one_or_default, except it returns stripped text contents of the found element
    """
    try:
        return element.select_one(selector).get_text().strip()
    except Exception as e:
        return default
    
def all_or_default(element, selector, default=[]):
    """Get all matching elements for a css selector within an element
    Params:
        - element: beautifulsoup element to search
        - selector: str css selector to search for
        - default: default value if there is an error or no elements found
    Returns:
        {list}: list of all matching elements if any are found, otherwise return
        the default value
    """
    try:
        elements = element.select(selector)
        if len(elements) == 0:
            return default
        return element.select(selector)
    except Exception as e:
        return default
    
def get_info(element, mapping, default=None):
    """Turn beautifulsoup element and key->selector dict into a key->value dict
    Args:
        - element: A beautifulsoup element
        - mapping: a dictionary mapping key(str)->css selector(str)
        - default: The defauly value to be given for any key that has a css
        selector that matches no elements
    Returns:
        A dict mapping key to the text content of the first element that matched
        the css selector in the element.  If no matching element is found, the
        key's value will be the default param.
    """
    return {key: text_or_default(element, mapping[key], default=default) for key in mapping}

def get_job_info(job):
    """
    Returns:
        dict of job's title, company, date_range, location, description
    """
    multiple_positions = all_or_default(
        job, '.pv-entity__role-details-container')

    # Handle UI case where user has muttiple consec roles at same company
    if (multiple_positions):
        company = text_or_default(job,
                                  '.pv-entity__company-summary-info > h3 > span:nth-of-type(2)')

        company_href = one_or_default(
            job, 'a[data-control-name="background_details_company"]')['href']
        pattern = re.compile('^/company/.*?/$')
        if pattern.match(company_href):
            li_company_url = 'https://www.linkedin.com/' + company_href
        else:
            li_company_url = ''
        multiple_positions = list(map(lambda pos: get_info(pos, {
            'title': '.pv-entity__summary-info-v2 > h3 > span:nth-of-type(2)',
            'date_range': '.pv-entity__date-range span:nth-of-type(2)',
            'location': '.pv-entity__location > span:nth-of-type(2)',
            'description': '.pv-entity__description'
        }), multiple_positions))
        for pos in multiple_positions:
            pos['company'] = company
            pos['li_company_url'] = li_company_url

        return multiple_positions

    else:
        job_info = get_info(job, {
            'title': '.pv-entity__summary-info h3:nth-of-type(1)',
            'company': '.pv-entity__secondary-title',
            'date_range': '.pv-entity__date-range span:nth-of-type(2)',
            'location': '.pv-entity__location span:nth-of-type(2)',
            'description': '.pv-entity__description',
        })
        company_href = one_or_default(
            job, 'a[data-control-name="background_details_company"]')['href']
        pattern = re.compile('^/company/.*?/$')
        if pattern.match(company_href):
            job_info['li_company_url'] = 'https://www.linkedin.com' + company_href
        else:
            job_info['li_company_url'] = ''

        return [job_info]
    
def get_school_info(school):
    """
    Returns:
        dict of school name, degree, grades, field_of_study, date_range, &
        extra-curricular activities
    """
    return get_info(school, {
        'name': '.pv-entity__school-name',
        'degree': '.pv-entity__degree-name span:nth-of-type(2)',
        'grades': '.pv-entity__grade span:nth-of-type(2)',
        'field_of_study': '.pv-entity__fos span:nth-of-type(2)',
        'date_range': '.pv-entity__dates span:nth-of-type(2)',
        'activities': '.activities-societies'
    })

def get_volunteer_info(exp):
    """
    Returns:
        dict of title, company, date_range, location, cause, & description
    """
    return get_info(exp, {
        'title': '.pv-entity__summary-info h3:nth-of-type(1)',
        'company': '.pv-entity__secondary-title',
        'date_range': '.pv-entity__date-range span:nth-of-type(2)',
        'location': '.pv-entity__location span:nth-of-type(2)',
        'cause': '.pv-entity__cause span:nth-of-type(2)',
        'description': '.pv-entity__description'
    })

def get_skill_info(skill):
    """
    Returns:
        dict of skill name and # of endorsements
    """
    return get_info(skill, {
        'name': '.pv-skill-category-entity__name',
        'endorsements': '.pv-skill-category-entity__endorsement-count'
    }, default=0)

def personal_info(soup):
        """Return dict of personal info about the user"""
        top_card = one_or_default(soup, 'section.pv-top-card-section')
        contact_info = one_or_default(soup, '.pv-contact-info')

        personal_info = get_info(top_card, {
            'name': '.pv-top-card-section__name',
            'headline': '.pv-top-card-section__headline',
            'company': '.pv-top-card-v2-section__company-name',
            'school': '.pv-top-card-v2-section__school-name',
            'location': '.pv-top-card-section__location',
            'summary': 'p.pv-top-card-section__summary-text'
        })

        image_div = one_or_default(top_card, '.profile-photo-edit__preview')
        image_url = ''
        # print(image_div)
        if image_div:
            image_url = image_div['src']
        else:
            image_div = one_or_default(top_card, '.pv-top-card-section__photo')
            style_string = image_div['style']
            pattern = re.compile('background-image: url\("(.*?)"')
            matches = pattern.match(style_string).groups()
            if matches:
                image_url = matches[0]

        personal_info['image'] = image_url

        return personal_info

def experiences(soup):
        """
        Returns:
            dict of person's professional experiences.  These include:
                - Jobs
                - Education
                - Volunteer Experiences
        """
        experiences = {}
        container = one_or_default(soup, '.background-section')

        jobs = all_or_default(
            container, '#experience-section ul .pv-position-entity')
        jobs = list(map(get_job_info, jobs))
        jobs = flatten_list(jobs)

        experiences['jobs'] = jobs

        schools = all_or_default(
            container, '#education-section .pv-education-entity')
        schools = list(map(get_school_info, schools))
        experiences['education'] = schools

        volunteering = all_or_default(
            container, '.pv-profile-section.volunteering-section .pv-volunteering-entity')
        volunteering = list(map(get_volunteer_info, volunteering))
        experiences['volunteering'] = volunteering

        return experiences
    
def skills(soup):
        """
        Returns:
            list of skills {name: str, endorsements: int} in decreasing order of
            endorsement quantity.
        """
        skills = soup.select('.pv-skill-category-entity__skill-wrapper')
        skills = list(map(get_skill_info, skills))

        # Sort skills based on endorsements.  If the person has no endorsements
        def sort_skills(x): return int(
            x['endorsements'].replace('+', '')) if x['endorsements'] else 0
        return sorted(skills, key=sort_skills, reverse=True)



def get_recommendations():
    
    tab = wd.find_elements_by_tag_name('artdeco-tab')
    expand = wd.find_elements_by_class_name('pv-profile-section__see-more-inline')
    
    #'show more' btn in the first tab item was clicked in scroll_to_bottom, we only need to click the 'show more' in the other items
    for item in tab[1:]:
        ActionChains(wd).move_to_element(item).click().perform()
        for btn in expand:
            try:
                ActionChains(wd).move_to_element(btn).click().perform()
            except:
                pass
            
    more = wd.find_elements_by_class_name('lt-line-clamp__more')
            
    for item in tab:
        ActionChains(wd).move_to_element(item).click().perform()
        for btn in more:
            try:
                wd.execute_script('arguments[0].disabled = true;',btn)
                wd.execute_script('arguments[0].click();',btn)
            except:
                pass
                
    
    soup = BeautifulSoup(wd.page_source,'html.parser') 
    recom = soup.find_all('artdeco-tabpanel') 
    
    recommend = []
    for panel in recom:
        recom_list = panel.find('ul',{'class':'section-info'}).find_all('li',{'class':'pv-recommendation-entity'})
        for item in recom_list:
            giver_intro = item.find('div',{'class':'pv-recommendation-entity__detail'}).get_text().strip().split('\n')
            giver_name = giver_intro[0].strip()
            giver_job = giver_intro[1].strip()
            companian_time = giver_intro[3].strip()
            giver_img = item.find('a',{'data-control-name':'recommendation_details_profile'})
            
            giver_recom = item.find('blockquote',{'class':'pv-recommendation-entity__text relative'}).get_text().strip().split('\n')[0].strip()
            '''recommend.append({
                'header':{
                    'name':
                }
            })'''
            
        
            
    
    
    
    

