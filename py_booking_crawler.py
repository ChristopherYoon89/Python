import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC  

url = "https://www.booking.com/"

checkin_month = "Oktober 2022"

checkin_day = "26, Friday"

#checkout_month = "June"

#checkout_day = "12"

chrome_driver_path = Service("C:/Users/User/Documents/Python_Developing/Python/Booking_Crawling/chromedriver")

df_dataset_counties = pd.read_csv('Counties2.csv', usecols=['Counties'])

df_properties = []

for row in df_dataset_counties.iterrows():
        county_search = row[1]['Counties']
        df_properties.append(county_search)

        try:
                driver.close()
        except Exception as e:
                print(e)

        try:
                driver = webdriver.Chrome(service=chrome_driver_path)
                driver.get(url)

                time.sleep(3)               

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


                results = wait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="property-card"]')))

                print(results)

                for property in results:
                        propertyArr = property.text.split("\n")
                        print(propertyArr)
                        df_properties.append(propertyArr)
                      
                while True:
                        time.sleep(3)
                        if not (driver.find_element(By.CSS_SELECTOR, "[aria-label='Next page']").is_enabled()):                         
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

print(df_mydata)

df_mydata.to_csv(r'Booking_Crawling_2_Adults_2_Kids.csv', header=False, index=False)
