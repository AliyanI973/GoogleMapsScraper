
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from parsel import Selector
import pandas as pd 
import time
import os

folder = "Data Files"

keyword = input("Keyword: ")
city = input("City: ")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-geolocation")

driver= webdriver.Chrome(options=chrome_options)
driver.maximize_window()
driver.get('https://www.google.com/maps/')


delay =5
wait = WebDriverWait(driver, delay)
time.sleep(2)


search_box = driver.find_element(By.CLASS_NAME, 'searchboxinput')
search_box.send_keys(f"{keyword} in {city}")

time.sleep(3)
search_button = driver.find_element(By.CLASS_NAME, 'mL3xi').click()

time.sleep(5)


def scrolling_feed(feed):

    prev_scroll_position = -1
    while True:
        
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", feed)
        
        time.sleep(8)

        current_scroll_position = driver.execute_script("return arguments[0].scrollTop", feed)        
        if current_scroll_position == prev_scroll_position:
            break

        prev_scroll_position = current_scroll_position

    page_source = driver.page_source

    with open("page_source.html", "w") as f:
        f.write(page_source)

        
feed_element = driver.find_element(By.XPATH, '//*[@role="feed"]')

scrolling_feed(feed_element)


time.sleep(20)

driver.quit()

data = []

def parse_items():

    with open('page_source.html', 'r') as f:
        feed_list = f.read()

    response= Selector(feed_list)

    data.clear()

    for res in response.xpath("//div[@class = 'lI9IFe ']"): # response is 114
        data.append ({
            "name": res.xpath(".//div[contains(@class,  'qBF1Pd')]/text()").get(default=None),
            
            "company_type": res.xpath(".//div[contains(@class, 'W4Efsd')]/span[1]/span/text()").get(default=None),
            
            "address": res.xpath(".//div[contains(@class, 'W4Efsd')]/span[2]/span[2]/text()").get(default=None),
            
            "phone_number": res.xpath(".//div[contains(@class, 'W4Efsd')][2]/span[2]/span[2]/text()").get(default=None),
            
            "website": res.xpath(".//div[contains(@class, 'Rwjeuc')]/div/a/@href").get(default=None)
            
        })

    df_places = pd.DataFrame(data)

    file_name = f"{keyword}_{city}.csv"

    if not os.path.isdir(folder):
        os.mkdir(folder)

    file_path= os.path.join(folder,file_name)

    df_places.to_csv(file_path, index=False)    

parse_items()

time.sleep(10)