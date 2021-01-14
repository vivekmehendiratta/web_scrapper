from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, WebDriverException
import time

import re

import secrets

def remove_nf_numbers(text):
    text = re.sub(r"[(][\d]{1,2}[)]", '', text)
    return text

class Linkedin:
    def __init__(self,username, password, path_to_driver):
        self.username=username
        self.password=password
        self.bot=webdriver.Chrome(path_to_driver)
    
    def login(self):
        bot=self.bot
        bot.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
        time.sleep(3)
        email=bot.find_element_by_id("username")
        email.send_keys(self.username)
        password=bot.find_element_by_id("password")
        password.send_keys(self.password)
        time.sleep(3)
        password.send_keys(Keys.RETURN)
        return
    
    def get_currentURL(self):
        return self.bot.current_url
    
    def search_profile(self, profile_name):
        bot = self.bot
        search = bot.find_element_by_css_selector("input[placeholder='Search']")
        time.sleep(3)
        search.click()
        search.send_keys(profile_name)
        time.sleep(3)
        search.send_keys(Keys.RETURN)
        time.sleep(10)
        

        profile_list = bot.find_elements_by_xpath("//div[@class='search-results-container']//ul//li//a[@href]")
        
        time.sleep(5)

        link_to_profile = profile_list[0].get_attribute('href')

        

        return link_to_profile

    def go_to_profile(self, profileURL):
        bot = self.bot
        bot.get(profileURL) 
        time.sleep(5)
        return
    
    def search_people(self):
        bot = self.bot 
        grid_list = bot.find_elements_by_xpath("//li[@class='org-page-navigation__item']//a")
        
        for x in grid_list:
            href = x.get_attribute('href')
            if 'people' in href:
                x.click()
        time.sleep(3)
        return

    def scroll_down(self):
        bot = self.bot

        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = bot.execute_script("return document.body.scrollHeight")

        i = 1000
        while i>0:
            # Scroll down to bottom
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = bot.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            i-=1
        
        return

    def get_all_profiles(self):
        bot = self.bot

        xpath = "//ul[@class='org-people-profiles-module__profile-list']//a"

        grid_list = bot.find_elements_by_xpath(xpath)
        
        profiles = [x.get_attribute('href') for x in grid_list]
        time.sleep(3)
        return list(set(profiles))
    
    def connect_to_profile(self, note = ''):
        bot = self.bot
        
        xpath = "//main[@class='core-rail']//section[@class='pv-top-card artdeco-card ember-view']//div[@class='display-flex']//button//span"

        title = bot.title
        title = remove_nf_numbers(title)
        name = title.split("|")[0].strip()

        note = f"Hi {name},\n" + note


        try:
            WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(2)
            
            add_note_xpath = "//button[@aria-label='Add a note']"
            WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, add_note_xpath))).click()
            time.sleep(2)

            message_area_path = "//div[@class='relative']//textarea[@name='message']"
            message_area = bot.find_element_by_xpath(message_area_path)
            message_area.send_keys(note)

            send_xpath = "//button[@aria-label='Send now']"
            WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, send_xpath))).click()
            time.sleep(2)

        except ElementClickInterceptedException:
            time.sleep(2)
            return 'fail'

        except TimeoutException:
            time.sleep(2)
            return 'fail'
        
        except WebDriverException:
            time.sleep(2)
            return 'web driver exception'
        
        return 'success'
