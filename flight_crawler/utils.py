import time
value_to_return = ""
def select_desire_month(_month, month_xpath,nb_xpath, driver,):
    global value_to_return
    text = driver.find_element_by_xpath(month_xpath)
    search_result = text.get_attribute("innerText").find(_month)
    
    if search_result != -1:
        value_to_return = True
    else:
        next_btn = driver.find_element_by_xpath(nb_xpath)
        is_disabled = next_btn.get_attribute('disabled')
    
        if is_disabled:
            value_to_return = "Date limit exception!"
        else:
            next_btn.click()
            time.sleep(1)
            select_desire_month(_month,month_xpath,nb_xpath,driver)

    return value_to_return