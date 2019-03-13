from metatype import Dict

from linkedin_driver import _login, __site_url__

from linkedin_driver.utils import (
    open_contact,
    scroll_to_bottom,
    open_interest,
    text_or_default_accomp,
    open_accomplishments,
    open_more,
    flatten_list,
    one_or_default,
    text_or_default,
    all_or_default,
    get_info,
    get_job_info,
    get_school_info,
    get_volunteer_info,
    get_skill_info,
    personal_info,
    experiences,
    skills,
    recommendations
)

from linkedin_driver.utils import (
    filter_contacts
)

from selenium.webdriver.support.wait import WebDriverWait

# misc
import bs4
import datetime
import metawiki
import requests

class Contact(Dict):

    @classmethod
    def _filter(cls, keyword=None):
        '''
        Returns:
            Iterator.
        '''
        if not cls._DRIVES:
            cls._DRIVES.append(_login())
        else:
            driver = cls._DRIVES[0]

        for item in filter_contacts(driver, keyword):
            yield(cls(item))

        driver.quit()
        raise NotImplemented

    @classmethod
    def _get(cls, url):

        driver = _login()

        record = {}

        # INTERESTS
        interests_data = open_interest(driver, url)
        record.update({'interests': interests_data})

        # CONTACT
        contact_data = open_contact(driver, url)
        record.update({'contact': contact_data})

        # <<SCROLL-DOWN>>
        scroll_to_bottom(driver, contact_url=url)

        # ACCOMPLISHMENTS
        accomplishments_data = open_accomplishments(driver)
        record.update({'accomplishments': accomplishments_data})

        # RECOMMENDATIONS
        recommendations_data = recommendations(driver)
        record.update({'recommendations':recommendations_data})

        # <<EXPAND-TABS>>
        open_more(driver)

        # PERSONAL-INFO
        soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        personal_info_data = personal_info(soup)
        record.update({'personal_info': personal_info_data})

        # EXPERIENCES
        experiences_data = experiences(soup)
        record.update({'experiences': experiences_data})

        # SKILLS
        skills_data = skills(soup)
        record.update({'skills': skills_data})

        # END
        driver.quit()

        return cls(record)


    def send_message(self):
        raise NotImplemented


class Post(Dict):

    @classmethod
    def _get(self, url):
        if not cls._DRIVES:
            cls._DRIVES.append(_login())
        else:
            driver = cls._DRIVES[0]

        driver.get(url)

    @classmethod
    def _filter(cls, limit=None, close_after_execution=True):

        if not cls._DRIVES:
            cls._DRIVES.append(_login())

        driver = cls._DRIVES[0]

        while True:

            soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
            posts_placeholder = soup.find('div', {'class': 'core-rail'})
            posts = posts_placeholder.find_all('div', {'class': 'relative ember-view'})

            count = 0

            for i, post in enumerate(posts):

                url = 'https://www.linkedin.com/feed/update/'+post.attrs['data-id']

                shared_by = post.find('div', {'class': 'presence-entity'})
                if shared_by:
                    shared_ = shared_by.find('div', {'class': 'ivm-view-attr__img--centered'})
                    if shared_:
                        shared_ = shared_.text
                        if shared_:
                            shared_by = shared_.strip()
                        else:
                            shared_by = shared_by.text.strip()
                    else:
                        shared_by = shared_by.text.strip()



                text = post.find('div', {'class': 'feed-shared-text'})
                if text is not None:
                    if isinstance(text, str):
                        text = text.strip()
                    else:
                        text = text.text.strip()
                else:
                    text = None

                mentioned_by = post.find('a', {'class': 'feed-shared-text-view__mention'})
                if mentioned_by:
                    profile_path = mentioned_by.attrs.get('href')
                    if profile_path:
                        mentioned_by = 'https://www.linkedin.com'+profile_path

                author_image = post.find('img', {'class': 'presence-entity__image'})
                if author_image is not None:
                    author_image = author_image.attrs['src']
                else:
                    author_image = None

                post_image = post.find('img', {'class': 'feed-shared-article__image'})
                if post_image is not None:
                    post_image = post_image.attrs['src']
                else:
                    post_image = None

                # author_image_data = requests.get(author_image)
                # post_image_data = requests.get(post_image)


                # comments =

                item = {
                    'url': url,
                    'date': None,
                    'body': text,
                    'media': {
                        'author_image': author_image,
                        'cover_image': post_image
                    },
                    'comments': [],
                    'mentioned_by': mentioned_by,
                    'shared_by': shared_by,
                    'logged': datetime.datetime.utcnow().isoformat(),
                    '-': url,
                    '+': metawiki.name_to_url(driver.metaname),
                    '*': metawiki.name_to_url('::mindey/topic#linkedin')
                }

                count += 1
                yield item

                if limit:
                    if count >= limit:
                        break

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    def _update(self):
        raise NotImplemented

    def add_comment(self, text):
        field = self.driver.find_element_by_class_name('mentions-texteditor__contenteditable')
        field.send_keys(text)
        button = self.driver.find_element_by_class_name('comments-comment-box__submit-button')
        button.click()



class Message(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented


class Comment(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented


class PostLike(dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented


class CommentLike(Dict):

    @classmethod
    def _get(self):
        raise NotImplemented

    @classmethod
    def _filter(self):
        raise NotImplemented

    def _update(self):
        raise NotImplemented

