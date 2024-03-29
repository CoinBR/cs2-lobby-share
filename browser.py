import os
import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from retrier import retry_until_ready
import cfg.browser as cfg

BROWSER_PROFILE = os.getenv('BROWSER_PROFILE', None)
    
class Browser():

    browser = None
    
    @classmethod
    def boot_if_needed(cls):
        if cls.browser is not None:
            return
           
        print("Launching Web Browser...")
        options = Options()

        if (BROWSER_PROFILE):
            options.add_argument("-profile")
            options.add_argument(cfg.firefox_profile_path)
            
        cls.browser = webdriver.Firefox(options)

    @classmethod
    def visit(cls, url):
        cls.boot_if_needed()
        cls.browser.maximize_window()
        cls.browser.switch_to.window(cls.browser.current_window_handle)
        cls.browser.get(url)

    @classmethod
    def lookup(cls, timeout=7):
        return Lookuper(cls.browser, timeout)

    
    @classmethod
    def lookupAll(cls, timeout=7):
        return MultipleLookuper(cls.browser, timeout)


class Lookuper():

    def __init__(self, browser, timeout):
        assert browser is not None
        assert timeout is not None
        assert timeout >= 0
        
        self.browser = browser
        self.timeout = timeout
        
    def text(self, text):
        xpath = f"//*[contains(text(), '{text}')]"
        return self.xpath(xpath)

    def button_or_link_with_text(self, text):
        xpath = f"//button[contains(text(), '{text}')] | //a[contains(text(), '{text}')]"
        return self.xpath(xpath)


    def img(self, src_value):
        xpath = f"//img[@src='{src_value}']"
        return self.xpath(xpath)

    def alt(self, alt_text):
        xpath = f"//*[@alt='{alt_text}']"
        return self.xpath(xpath)

    def xpath(self, xpath):
        return self.by(By.XPATH, xpath)
    
    def css(self, css):
        return self.by(By.CSS_SELECTOR, css)

    def by(self, by, value):
        return Selector(self.browser, by, value, self.timeout)

class MultipleLookuper(Lookuper):
    
    def by(self, by, value):
        return MultipleSelector(self.browser, by, value, self.timeout)
    

class _BaseSelector():
    
    def __init__(self, browser, by, value, timeout):
        assert browser is not None
        assert by is not None
        assert value is not None
        assert timeout is not None
        assert timeout >= 0
        
        self.browser = browser
        self.by = by
        self.value = value
        self.timeout = timeout

    def _wait_for_element(self):
        assert self.browser is not None, "Must visit a page before finding its elements"
        WebDriverWait(self.browser, self.timeout).until(
                EC.element_to_be_clickable((self.by, self.value)))
     

class Selector(_BaseSelector):
    
    @retry_until_ready(timeout=7)
    def click(self):
        self.find().click()
     
    def exists(self):
        try:
            find()
            return True
        except:
            return False

    @retry_until_ready(timeout=7)
    def find(self):
        self._wait_for_element()
        return self.browser.find_element(self.by, self.value)

 

class MultipleSelector(_BaseSelector):
    
    def click(self):
        self.forEach(
                     lambda x: x.click())

    def forEach(self, action):
        elements = self.browser.find_elements(self.by, self.value)

        for element in elements:
            action(element)

        
