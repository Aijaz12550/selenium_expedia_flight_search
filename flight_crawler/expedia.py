from selenium.webdriver import Chrome, ChromeOptions
from flight_crawler import utils
from django.http import HttpResponse
import os
import json
import time
import logging
from rest_framework.decorators import api_view


@api_view(["GET", "POST"])
def expedia_flights(request):
    driver = Chrome("chromedriver")
    driver.set_window_size(1000, 1000)
    try:
        
        result = []
    
        logging.basicConfig(level=logging.INFO)
        logging.info(request.body)

        body_data = json.loads(request.body)
        
        fly_from = body_data['fly_from']
        fly_to = body_data['fly_to']
        fly_day = body_data['fly_day']
        fly_month = body_data['fly_month']
        fly_year = body_data['fly_year']

        logging.info( fly_from)
        logging.info(fly_to)
        
        driver.get("https://www.expedia.com/?flightType=oneway")
        
        flights_tab = driver.find_elements_by_class_name('uitk-tab-anchor')
        flights_tab[1].click()
        
        time.sleep(1)
        
        s = driver.find_element_by_xpath('//*[@id="uitk-tabs-button-container"]/div/li[2]/a')
        s.click()
        
        select_from_btn = driver.find_element_by_xpath('//*[@id="wizard-flight-tab-oneway"]/div[2]/div[1]/div/div[1]/div')
        select_from_btn.click()
        
        time.sleep(1)
        
        
        leaving_from_ = driver.find_element_by_xpath('//*[@id="location-field-leg1-origin"]')
        leaving_from_.send_keys(fly_from)
        driver.find_element_by_xpath('//*[@id="location-field-leg1-origin-menu"]/div[2]/ul/li[1]/button').click()
        
        time.sleep(1)
    
        going_to_btn = driver.find_element_by_xpath('//*[@id="location-field-leg1-destination-menu"]/div[1]/button')
        going_to_btn.click()
        
        going_to_input = driver.find_element_by_xpath('//*[@id="location-field-leg1-destination"]')
        going_to_input.send_keys(fly_to)
        driver.find_element_by_xpath('//*[@id="location-field-leg1-destination-menu"]/div[2]/ul/li[1]/button').click()
        
        
        # select date
        date_btn = driver.find_element_by_xpath('//*[@id="d1-btn"]')
        date_btn.click()
        
        time.sleep(1)
        
        # calender
        month_xpath = '//*[@id="wizard-flight-tab-oneway"]/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div[1]'
        nb_xpath = '//*[@id="wizard-flight-tab-oneway"]/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/div[1]/button[2]'
        response_ = utils.select_desire_month(f"{fly_month} {fly_year}", month_xpath, nb_xpath, driver)
        
        if response_ == "Date limit exception!":
            driver.close()
            return HttpResponse(json.dumps({"statusCode":404,"error":"Date Limit, Decrease your date"}), content_type ="application/json")
        else:
        
            # selecting exact day 
            # suppose day is 2


            b = '//*[@id="wizard-flight-tab-oneway"]/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[2]/td[4]/button'
    
            select_day = driver.find_element_by_xpath(b)

            for row in range(6):
                flag = False
                for j in range(7):
                     
                    bd = f'//*[@id="wizard-flight-tab-oneway"]/div[2]/div[2]/div/div/div/div/div[2]/div/div[2]/div[2]/div[1]/table/tbody/tr[{row+1}]/td[{j+1}]/button'

                    try:
                        select_day1 = driver.find_element_by_xpath(bd)
                        
                        if select_day1.get_attribute("data-day") == fly_day:
                            select_day1.click()
                            print("DATE FOUND")
                            flag = True
                            break
                    except:
                        print("X_PATH NOT FOUND")
                if flag:
                    break
            
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="wizard-flight-tab-oneway"]/div[2]/div[2]/div/div/div/div/div[2]/div/div[3]/button').click()
        
            logging.info(driver.current_url)
            search_btn = driver.find_element_by_xpath('//*[@id="wizard-flight-pwa-1"]/div[3]/div[2]/button')
            search_btn.click()
            time.sleep(1)
            flights_data_element = driver.find_elements_by_class_name("uitk-card-link")
            time.sleep(2)
            i = 0
            for flight in flights_data_element:
                i += 1
                flight_text = flight.get_attribute('innerText').split(", ")[0:4:3] # slicing the incoming text
                result.append({"carrier":flight_text[0].replace("Select and show fare information for ",""), "price": flight_text[1].replace(" One way per traveler","").replace("Priced at ",""), "sort_id":i, "site":"expedia", "sort_by":"lowest price" })
                logging.info(flight_text)
            
        
            time.sleep(1)
            driver.close()
    
            return HttpResponse(json.dumps({"statusCode":200,"data":result}), content_type ="application/json")
    except:
        logging.basicConfig(level=logging.ERROR)
        logging.error("Error")
        return HttpResponse(json.dumps({"statusCode": 502, "message":"Error in Script or Expedia."}))
        driver.close()
    