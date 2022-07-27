from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


driver = webdriver.Chrome("E:\python\data_collect\data_ml_pr\chromedriver.exe")



driver.get("https://nid.naver.com/nidlogin.login?url=http://section.cafe.naver.com")
time.sleep(1)


driver.find_element_by_id("ones").click()
user_id = driver.find_element_by_id("disposable")
user_id.send_keys("67311754")
driver.find_element_by_id("otnlog.login").click()
time.sleep(2)


driver.get("https://cafe.naver.com/healingdogcat")
driver.implicitly_wait(3)

driver.find_element_by_name('query').send_keys('낙상')
driver.find_element_by_name("query").send_keys(Keys.ENTER)
time.sleep(2)

driver.switch_to.frame("cafe_main")

driver.find_element_by_xpath("/html/body/div[1]/div/div[5]/table/tbody/tr[2]/td[1]/div[2]/div/a[1]").send_keys(Keys.ENTER)
