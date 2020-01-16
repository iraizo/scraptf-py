from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import re
import time 
from parsel import Selector
from random import choice
import random
import requests
from bs4 import BeautifulSoup
url = "https://scrap.tf/raffles/ending"

def exists(class_name):
    try:
        driver.find_element_by_class_name(class_name)
    except NoSuchElementException:
        return False
    return True

driver = webdriver.Firefox()
def login():
    driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
    driver.get("https://scrap.tf/login/")
    print("waiting for login")
    (WebDriverWait(driver, 100).until(expected_conditions.title_contains("Scrap.TF")))
    print("joining raffles..")
    #rafflejoin()
urls = []
def createlist(ids):
    global urls
    for id in ids:
        urls.append("https://scrap.tf/raffles/" + id)

login()
driver.get("https://scrap.tf/raffles/ending")
SCROLL_PAUSE_TIME = 0.5
html = driver.find_element_by_tag_name('html')
last_height = driver.execute_script("return document.body.scrollHeight")
y = 1000
for timer in range(0, 15):
    driver.execute_script("window.scrollTo(0, "+str(y)+")")
    if(exists("panel-body raffle-pagination-done") == True):
        print("Loaded all raffles")
        break
    y += 1000 
    time.sleep(1)

id_dump = []
def filterdiv(divs): 
    global id_dump
    for div in divs:
        id_ = div.strip("raffle-box")
        id_dump.append(id_)

html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
parse = BeautifulSoup(html, 'html.parser')
selector = Selector(text=html)
divs = selector.css('.panel-raffle::attr(id)').getall()

count = 0
filterdiv(divs)
createlist(id_dump)
print(urls)

def rafflejoin():
    global count
    try:
        visit = random.choice(urls)
    except IndexError as e:
        print("Index error: All raffles joined.")
    else:
        time.sleep(2) 
        driver.get(visit)
        urls.remove(visit)
        if(exists("raffle-start-time") == True):
            print("Raffle ended, retrying")
            rafflejoin()
        else:
            button = driver.find_element_by_id("raffle-enter")
            text = button.get_attribute("data-loading-text")    
            if text != "Leaving...":
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    button.click()
                    count += 1
                    print("Raffles joined: {}".format(count))
                    rafflejoin()
                except Exception as e:
                    print("Error: {}, retrying".format(e))
                    rafflejoin()
            else:
                print("raffle already joined retrying")
                rafflejoin()


rafflejoin()