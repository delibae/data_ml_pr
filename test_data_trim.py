import sys    # 시스템
import os     # 시스템

import pandas as pd    # 판다스 : 데이터분석 라이브러리
import numpy as np     # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup     # html 데이터 전처리
from selenium import webdriver    # 웹 브라우저 자동화
from selenium.webdriver.common.keys import Keys #셀레니움 keys
import time                       # 시간 지연
import math

driver = webdriver.Chrome("E:\python\data_collect\data_ml_pr\chromedriver.exe")

# 네이버 일회용 로그인
driver.get("https://nid.naver.com/nidlogin.login?url=http://section.cafe.naver.com")
time.sleep(1)

pw = "20539333"

driver.find_element_by_id("ones").click()
user_id = driver.find_element_by_id("disposable")
user_id.send_keys(pw)
driver.find_element_by_id("otnlog.login").click()
time.sleep(2)

# 사이트 주소
driver.get("https://cafe.naver.com/healingdogcat")
time.sleep(2)


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
    # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
# print(title)
content_tags = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer').select('p')

content_tags = [ tags.get_text() for tags in content_tags ]
content_tags = content_tags[8:]
content_tags.remove('\u200b')
content = ' '.join(content_tags)

print(content)
#     # dict형태로 만들어 결과 list에 저장
# res_list.append({'title' : title, 'content' : content})
    # time.sleep 작업도 필요하다.

driver.close()



# for link in href_list:
#     print(link*10)
#     driver.get(link)
#     driver.switch_to.default_content()
#     content = driver.find_element_by_tag_name("iframe")
#     print(content)
#     driver.switch_to.frame(content)

#     driver.switch_to.frame("cafe_main")
#     res_list = []
#     # Beautifulsoup 활용
#     # article도 switch_to.frame이 필수
#     time.sleep(2)
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     # 게시글에서 제목 추출
#     title = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').get_text()
#     # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
#     content_tags = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer > div:nth-child(2) > div.content.CafeViewer > div').select('p')
#     content = ' '.join([ tags.get_text() for tags in content_tags ])
#     # dict형태로 만들어 결과 list에 저장
#     res_list.append({'title' : title, 'content' : content})
#     # time.sleep 작업도 필요하다.
#     driver.close()


