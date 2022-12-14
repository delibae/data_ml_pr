
import sys    # 시스템
import os     # 시스템

import pandas as pd    # 판다스 : 데이터분석 라이브러리
import numpy as np     # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup     # html 데이터 전처리
from selenium import webdriver    # 웹 브라우저 자동화
from selenium.webdriver.common.keys import Keys #셀레니움 keys
import time                       # 시간 지연
import math

keyword = "눈+피부+귀"

# 크롬 웹브라우저 실행
driver = webdriver.Chrome("E:\python\data_collect\data_ml_pr\chromedriver.exe")

# 네이버 일회용 로그인
driver.get("https://nid.naver.com/nidlogin.login?url=http://section.cafe.naver.com")
time.sleep(1)

pw = "85744570"

driver.find_element_by_id("ones").click()
user_id = driver.find_element_by_id("disposable")
user_id.send_keys(pw)
driver.find_element_by_id("otnlog.login").click()
time.sleep(2)

# 사이트 주소
driver.get("https://cafe.naver.com/healingdogcat")
time.sleep(2)

# 게시판 클릭
driver.find_element_by_link_text(keyword).click()

# driver.find_element_by_name('query').send_keys('테슬라')
# driver.find_element_by_name("query").send_keys(Keys.ENTER)
# time.sleep(2)

# 게시판 프레임 접근
driver.switch_to.frame("cafe_main")

# 게시글 50개씩
driver.find_element_by_css_selector("#listSizeSelectDiv").click()
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[4]/ul/li[7]/a").click()

driver.get("https://cafe.naver.com/healingdogcat/814015")

# driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/table/tbody/tr[5]/td[1]/div[2]/div/a[1]").click()

res_list = []
# Beautifulsoup 활용
# article도 switch_to.frame이 필수

time.sleep(2)
driver.switch_to.frame("cafe_main")
soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 게시글에서 제목 추출
title = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').get_text()

print(title)

    # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
content_tags = soup.select_one('#SE-728fbbcb-c2ea-4331-8311-15d9c09658bb').select('p')
content = ' '.join([ tags.get_text() for tags in content_tags ])
    # dict형태로 만들어 결과 list에 저장
res_list.append({'title' : title, 'content' : content})
    # time.sleep 작업도 필요하다.
# driver.close()

# print(res_list)
print(title)
print(content_tags)
print(res_list)

driver.get("https://cafe.naver.com/ArticleRead.nhn?clubid=25273665&page=1&userDisplay=50&menuid=44&boardtype=L&articleid=814061&referrerAllArticles=false")

# driver.find_element_by_xpath("/html/body/div[1]/div/div[4]/table/tbody/tr[5]/td[1]/div[2]/div/a[1]").click()

res_list = []
# Beautifulsoup 활용
# article도 switch_to.frame이 필수

time.sleep(2)
driver.switch_to.frame("cafe_main")
soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 게시글에서 제목 추출
title = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').get_text()
    # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
content_tags = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer > div:nth-child(2) > div.content.CafeViewer > div').select('p')
content = ' '.join([ tags.get_text() for tags in content_tags ])
    # dict형태로 만들어 결과 list에 저장
res_list.append({'title' : title, 'content' : content})
    # time.sleep 작업도 필요하다.
driver.close()

# print(res_list)
print(title)
print(content_tags)
print(res_list)

