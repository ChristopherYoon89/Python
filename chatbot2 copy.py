import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import os
from blacklist import domains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver.v2 as uc
from selenium.webdriver.support.ui import WebDriverWait as wait 
from selenium.webdriver.support import expected_conditions as EC    


class My_Chrome(uc.Chrome):
    def __del__(self):
        pass

options = uc.ChromeOptions() 

options.add_argument("--mute-audio")

driver = My_Chrome(options=options)

chatlink = 'https://www.youtube.com/watch?v=vKpnXiSFXcE' 


# cd C:\Users\User\Documents\Python Developing\Python\Chat_Bot

#export PATH=$C:\Users\User\Documents\Python Developing\Python\Chat_Bot\geckodriver

# Open duckduckgo, search for keyword, return page_source """

#driver = webdriver.Chrome()


driver.implicitly_wait(10)

        #driver.get("https://duckduckgo.com")
        #search_field = driver.find_element_by_id('search_form_input_homepage')
        #search_field.clear()

        #search_field.send_keys(keyword)
        #search_field.submit()

driver.get("https://www.youtube.com")

driver.implicitly_wait(10)  




# Accept Cookies of YouTube 

accept_cookies = driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[2]/div[2]/div[5]/div[2]/ytd-button-renderer[2]") # note find_elements with an 's'

accept_cookies.click()

driver.implicitly_wait(10)  

# Click on Anmelden


anmelden = driver.find_element(By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a")

driver.execute_script("arguments[0].click();", anmelden)

driver.implicitly_wait(10)  

time.sleep(5)


# Enter Email adress

Input_Field = driver.find_element(By.ID, "identifierId")

Input_Field.send_keys("xxxx.yyyyyy@gmail.com")


driver.implicitly_wait(10)  
time.sleep(7)


# Click on NEXT 

click_next1 = driver.find_element(By.ID, "identifierNext") 

driver.execute_script("arguments[0].click();", click_next1)


driver.implicitly_wait(10) 

time.sleep(6)

# Enter PASSWORD

Input_Field = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")

Input_Field.send_keys("Z######")


driver.implicitly_wait(10)  


# Klick NEXT2

click_next2 = driver.find_element(By.ID, "passwordNext") 

driver.execute_script("arguments[0].click();", click_next2)


driver.implicitly_wait(10) 


# Go to url of video stream on youtube


driver.get(chatlink)

driver.implicitly_wait(10)

time.sleep(12)


# Click on Anmelden


anmelden = wait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a")))

#anmelden = driver.find_element(By.XPATH, "/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[3]/div[2]/ytd-button-renderer/a")

driver.execute_script("arguments[0].click();", anmelden)

driver.implicitly_wait(10)  

time.sleep(8)

driver.get(chatlink)

time.sleep(5) 


# Switch to chatframe, insert quote and press send button  


wait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"chatframe")))

enter_string2 = wait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/iron-pages/div[1]/yt-live-chat-message-input-renderer/div[1]/div[1]/div/yt-live-chat-text-input-field-renderer/div[1]")))

enter_string2.click()

df_dataset = pd.read_csv('DATA_FINAL_BELOW200.csv', usecols=['Quote'])

print(df_dataset)


for row in df_dataset.iterrows():
        quote = row[1]['Quote']
        try:                
                enter_string2.send_keys(quote)

                post_button = wait(driver,20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/iron-pages/div[1]/yt-live-chat-message-input-renderer/div[1]/div[3]/div[2]/div[2]")))

                post_button.click()

                enter_string2.click()

                time.sleep(120)
        except Exception as e:
                print(e)




driver.close()









