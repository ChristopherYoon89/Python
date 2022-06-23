import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import sys
from selenium.webdriver.support import expected_conditions as EC  

url = "https://www.booking.com/index.en-gb.html?label=gen173nr-1FCAEoggI46AdIM1gEaGmIAQGYATG4ARjIAQzYAQHoAQH4AQKIAgGoAgS4AoKptJQGwAIB0gIkNzBlZDAxYzMtOGM3ZS00ZDRhLTkyMWQtYmE2YzFmYWYxM2Fh2AIF4AIB&sid=88f90169f82312c259e1da039f387404&sb_price_type=total;srpvid=47977de8d0e900e5&;changed_currency=1;selected_currency=EUR"

#county_search = "Dublin"

checkin_month = "Oktober 2022"
#checkout_month = "June"
checkin_day = "26, Friday"
#checkout_day = "12"

chrome_driver_path = Service("C:/Users/User/Documents/Python_Developing/Python/Booking_Crawling/chromedriver")

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-logging"])




df_dataset_counties = pd.read_csv('Counties2.csv', usecols=['Counties'], sep=',')

df_properties = []

for row in df_dataset_counties.iterrows():
        county_search = row[1]['Counties']
        df_properties.append(county_search)

        try:
                driver.close()
        except Exception as e:
                print(e)


        try:
                driver = webdriver.Chrome(options=options, service=chrome_driver_path)
                driver.get(url)

                time.sleep(3)

                #choose_currency = driver.find_element(By.CSS_SELECTOR, "div.bui-group__item:nth-child(1) > button:nth-child(1)")

                #choose_currency.click()

                #choose_currency_euro = wait(driver,20).until(EC.presence_of_element_located((By.LINK_TEXT , "Euro")))

               

                search_entry = wait(driver,20).until(EC.presence_of_element_located((By.ID, "ss")))

                search_entry.send_keys(county_search)


                # Find and select checkin date

                Datebox_checkin_month = driver.find_element(By.CSS_SELECTOR, ".xp__dates__checkin > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > select:nth-child(2)")

                Datebox_checkin_month.send_keys(checkin_month)

                Datebox_checkin_day = driver.find_element(By.CSS_SELECTOR, ".xp__dates__checkin > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > select:nth-child(2)")

                Datebox_checkin_day.send_keys(checkin_day)


                time.sleep(3)


                # Find and select checkout date 

                #Datebox_checkout_month = driver.find_element(By.CSS_SELECTOR, ".xp__dates__checkout > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > select:nth-child(2)")

                #Datebox_checkout_month.send_keys(checkout_month)

                #Datebox_checkout_day = driver.find_element(By.CSS_SELECTOR, ".xp__dates__checkout > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > select:nth-child(2)")

                #Datebox_checkout_day.send_keys(checkout_day)


                #time.sleep(4)


                # Find and select number of persons 

                Number_of_guests = driver.find_element(By.CSS_SELECTOR, ".xp__guests")

                Number_of_guests.click()

                time.sleep(2)

                #subract_adult_button = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sb-group__field:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(2)")))

                #subract_adult_button.click()


                add_child_button = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.sb-group__field:nth-child(2) > div:nth-child(1) > div:nth-child(2) > button:nth-child(4)")))

                add_child_button.click()

                time.sleep(1)

                add_child_button.click()

                time.sleep(2)


                age_child1_input = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sb-group__children__field > select:nth-child(1)")))

                age_child1_input.send_keys("10")

                time.sleep(2)

                age_child2_input = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sb-group__children__field > select:nth-child(2)")))

                age_child2_input.send_keys("10")

                time.sleep(2)

                # Submit search button

                Submit_button = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sb-searchbox__button")))

                Submit_button.click()

                time.sleep(3)


                #results = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="property-card"]')))


                results = driver.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')

                print(results)

                for property in results:
                        propertyArr = property.text.split("\n")
                        print(propertyArr)
                        df_properties.append(propertyArr)
                        


                while True:
                        time.sleep(3)
                        elm_check = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Next page']")
                        if not (driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']").is_enabled()): # or len(elm_check) < 1:
                                
                                break
                        
                        elm = driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']") 
                        elm.click()
                        time.sleep(3)
                        results = driver.find_elements(By.CSS_SELECTOR, '[data-testid="property-card"]')

                        print(results)

                        for property in results:
                                propertyArr = property.text.split("\n")
                                print(propertyArr)
                                df_properties.append(propertyArr)  

                
                        
                                

        except Exception as e:
                print(e)







df_mydata = pd.DataFrame(df_properties)

#df_mydata.columns = ['HTML_Text', 'Name_of_hotel', 'HTML_Text2', 'HTML_Text3', 'Location', 'Additional_info', 'Rating', 'Rating2', 'Number_of_Ratings', 
#'Additional_info2', 'Additional_info3', 'Additional_info4', 'No_of_beds', 'Cancellation', 'Additional_info5', 'No_of_guests_per_night', 'Price_per_night', 
#'Additional_info6', 'HTML_Text4', 'HTML_Text5', 'HTML_Text6', 'HTML_Text7']

#df_mydata.dropna(inplace=True)

print(df_mydata)

df_mydata.to_csv(r'2_Adults_2_Kids_August_26_27.csv', header=False, index=False)


