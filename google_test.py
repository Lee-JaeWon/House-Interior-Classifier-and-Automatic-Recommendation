from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path='chromedriver')
driver.maximize_window()

url = "https://www.google.com"
url2 = "https://ohou.se/"
url3 = "https://mall.hanssem.com/main.html"

driver.get(url2)



style = "modern"
factor = "warm"
furniture = "의자"
search_word = style + "하고, " + factor + "한 " + furniture

print(search_word)

time.sleep(0.5) ## 0.5초

# element = driver.find_element_by_name('q')
# element = driver.find_element_by_id("global-search-combobox")
# element = driver.find_element_by_id("_searchKey")
element = driver.find_element_by_class_name("css-16px0cl")
element.send_keys(search_word)

# element.submit()
element.send_keys(Keys.RETURN)

while(True):
    pass