from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait       
from selenium.webdriver.common.by import By       
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, WebDriverException
import time

import re

import secrets

def clean_title(text):
    text = re.sub(r"[(][\d]{1,2}[)]", '', text)
    text = re.sub(r'(^\w{2,3}\. ?)', r'', text)
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

    def scroll_down(self, scroll_counter=1000):
        bot = self.bot

        SCROLL_PAUSE_TIME = 3

        # Get scroll height
        last_height = bot.execute_script("return document.body.scrollHeight")

        i = scroll_counter
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

        # xpath = "//ul[@class='org-people-profiles-module__profile-list']//a"

        xpath = ".//ul[@class='display-flex list-style-none flex-wrap']//a"

        grid_list = bot.find_elements_by_xpath(xpath)
        
        profiles = [x.get_attribute('href') for x in grid_list]
        time.sleep(3)
        return list(set(profiles))
    
    def checkConnection(self):
        bot = self.bot
        # follow_xpath = ".//div[@class='display-flex']//button//*[contains(.,'Follow')]"
        # connect_xpath = ".//div[@class='display-flex']//button//*[contains(.,'Connect')]"
        # pending_xpath = ".//div[@class='display-flex']//button//*[contains(.,'Pending')]"
        # message_xpath = ".//div[@class='display-flex']//button//*[@type='lock-icon']//*[contains(.,'Message')]"
        # message_xpath_connected = ".//div[@class='display-flex']//*[contains(.,'Message')]"

        follow_xpath = ".//div[contains(@class,'display-flex')]//button//*[contains(.,'Follow')]"
        connect_xpath = ".//div[contains(@class,'display-flex')]//button//*[contains(.,'Connect')]"
        pending_xpath = ".//div[contains(@class,'display-flex')]//button//*[contains(.,'Pending')]"
        message_xpath = ".//div[contains(@class,'display-flex')]//button//*[@type='lock-icon']"
        message_xpath_connected = ".//div[contains(@class,'display-flex')]//*[contains(.,'Message')]"

        try:
            
            follow_element = bot.find_element_by_xpath(follow_xpath)
            if follow_element.text == 'Follow':
                print('Found follow element')
                return 'follow'
        except Exception as e:
            try:
                
                ele = bot.find_element_by_xpath(pending_xpath)
                if ele.text == 'Pending':
                    print('Found pending element')
                    return 'pending'
            except Exception as e:
                try:
                    
                    ele = bot.find_element_by_xpath(connect_xpath)
                    if ele.text == 'Connect':
                        print('found connect element')
                        return 'connect'
                except Exception:
                    try:
                        
                        ele = bot.find_element_by_xpath(message_xpath)
                        print("found locked message")
                        if ele.text == 'Message':
                            return 'locked'
                    except Exception as e:
                        try:
                            ele = bot.find_element_by_xpath(message_xpath_connected)
                            print('profile connected, returning True')
                            return 'connected'
                        except Exception as e:
                            print(e)
        return 'error'

    def connect_to_profile(self, note = ''):
        bot = self.bot
        

        # xpath = "//main[@class='core-rail']//section[@class='pv-top-card artdeco-card ember-view']//div[@class='display-flex']//button//span"
        xpath = ".//div[contains(@class,'display-flex')]//button//*[contains(.,'Connect')]"

        title = bot.title
        title = clean_title(title)
        name = title.split("|")[0].strip()
        name = name.split()[0].strip().title()

        note = f"Hi {name},\n" + note

        try:
            WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
            time.sleep(2)
            
            add_note_xpath = ".//button[@aria-label='Add a note']"
            WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, add_note_xpath))).click()
            time.sleep(2)

            message_area_path = ".//div[contains(@class,'relative')]//textarea[contains(@name,'message')]"
            message_area = bot.find_element_by_xpath(message_area_path)
            message_area.send_keys(note)
            time.sleep(2)

            send_xpath = ".//button[@aria-label='Send now']"
            WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, send_xpath))).click()
            time.sleep(2)

        except ElementClickInterceptedException:
            print('ElementClickInterceptedException')
            time.sleep(2)
            return 'fail'

        except TimeoutException:
            print('TimeoutException')
            time.sleep(2)
            return 'fail'
        
        except WebDriverException:
            print('WebDriverException')
            time.sleep(2)
            return 'web driver exception'
        
        return 'success'

    def connect_to_profile_again(self, note = ''):
        bot = self.bot
        
        xpath = "//section[@class='pv-top-card artdeco-card ember-view']//div[@class='display-flex']//div[@class='artdeco-dropdown__content-inner']//*[contains(.,'Connect')]"

        element = bot.find_element_by_xpath(xpath)
        bot.execute_script("arguments[0].click();", element)
        # element.click()

        title = bot.title
        title = clean_title(title)
        name = title.split("|")[0].strip()
        name = name.split()[0].strip()

        note = f"Hi {name},\n" + note

        # WebDriverWait(bot, 20).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        # time.sleep(2)


        return

    def end_session(self):
        bot = self.bot

        bot.quit()
        return
    
    