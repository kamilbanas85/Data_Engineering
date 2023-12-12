import pandas as pd
from selenium import webdriver
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
import os

import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from selenium import webdriver

################################################################################################
#%%

main_login_url = 'xxx'
Username = 'login'
Password = 'password'

timeouts={'implicit':25000,
           'pageLoad':25000,
           'script':25000}

################################################################################################
#%%

path =  '/tmp/geckodriver'

options = Options()
options.headless = True 
#options.binary_location = FirefoxBinary('/usr/bin/firefox')

service = Service(executable_path= path)
  
#options1.page_load_strategy= "eager"
    
options.timeouts=timeouts


################################################################################################
#%%

driver = webdriver.Chrome()

################################################################################################
#%%

# login
driver.get(main_login_url)
    
u = driver.find_element("name",'Username')
u.send_keys(Username)
p = driver.find_element("name",'Password')
p.send_keys(Password)
#p.send_keys(Keys.RETURN)
    
driver.find_element("id","login-button").click()

time.sleep(20)

WebDriverWait(driver=driver, timeout=10).until(
    lambda x: x.execute_script("return document.readyState === 'complete'")
    )
    
errors = driver.find_elements("class name","flash-error")
error_message = "Incorrect username or password."
    
for e in errors:
         print(e.text)

if any(error_message in e.text for e in errors):
    print("[!] Login failed")
    driver.close()
else:
    print("[+] Login successful") 


driver.close()
