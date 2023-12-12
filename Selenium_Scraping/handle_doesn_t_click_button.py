from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException

#%%
download_files_directory = "/tmp/"

options = Options()
options.add_argument('--headless')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
prefs = {'download.default_directory' : download_files_directory}
options.add_experimental_option('prefs', prefs)

#%%

driver = webdriver.Chrome(service=Service('/tmp/my_chromedriver/chromedriver-linux64/chromedriver'), options=options)
driver.get(main_url)

######################################################################
#%% click button

wait = WebDriverWait(driver, 20)

try:
        # showmore_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Download")))
        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, '..xpath..')))
        showmore_link.click()

except ElementClickInterceptedException:
        print("Trying to click on the button again")
        driver.execute_script("arguments[0].click()", showmore_link)

time.sleep(20)
driver.close()
