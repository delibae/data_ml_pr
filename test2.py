

# 공지 숨겨도 크롤링에 포함됨
# 공지 숨기기 클릭
# anno_off = driver.find_element_by_css_selector('.check_box').click()

### Step 0. 준비
import sys    # 시스템
import os     # 시스템

import pandas as pd    # 판다스 : 데이터분석 라이브러리
import numpy as np     # 넘파이 : 숫자, 행렬 데이터 라이브러리

from bs4 import BeautifulSoup     # html 데이터 전처리
from selenium import webdriver    # 웹 브라우저 자동화
from selenium.webdriver.common.keys import Keys #셀레니움 keys
import time                       # 시간 지연
import math

## Step 1. 크롤링
keyword = "눈+피부+귀"
# crawling_no = int(input('클롤링 할 글 개수를 입력 :'))

crawling_no = 3


# 크롬 웹브라우저 실행
driver = webdriver.Chrome("E:\python\data_collect\data_ml_pr\chromedriver.exe")

# 네이버 일회용 로그인
driver.get("https://nid.naver.com/nidlogin.login?url=http://section.cafe.naver.com")
time.sleep(1)


driver.find_element_by_id("ones").click()
user_id = driver.find_element_by_id("disposable")
user_id.send_keys("64869811")
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

crawling_list = []
no_app = []
title_app = []
nick_app  = []
like_app  = []
content_app = []


# 크롤링 해야 할 페이지 계산
crawling_page = int(math.ceil(crawling_no / 50)+1)

# html = browser.page_source
# soup = BeautifulSoup(html,'html.parser')

# content = [soup.select('div.ContentRender')[0].text]
# content_app.append(content)
try: 

    for page in range(1,crawling_page):
        # 페이지 클릭
        driver.find_element_by_link_text(str(page)).click()
        time.sleep(1)
        #soup 초기화

        # 글 번호 수집
        no = [i.text for i in driver.find_elements_by_css_selector('.td_article')]
        no_split = [ni.split()[0] for ni in no]
        # 글 제목 수집
        title = [i.text for i in driver.find_elements_by_css_selector('.article')]
        # 글 내용 수집

        # 작성자 수집
        nick = [i.text for i in driver.find_elements_by_css_selector('.p-nick .m-tcol-c')]
        # 좋아요 수집
        like = [i.text for i in driver.find_elements_by_css_selector('.td_likes')]
        # 수집 데이터 append
        no_app.append(no_split)
        title_app.append(title)

        nick_app.append(nick)
        like_app.append(like)
        # 10페이지 마다 프린트 & 다음 페이지로 클릭
        if str(page)[-1] == '0':
            print(int(page), 'page 크롤링 완료')
            driver.find_element_by_link_text('다음').click()
# 더이상 페이지가 존재하지 않을 시
except:
    print('더이상 페이지가 존재하지 않음')

driver.close()
    
# 리스트안 리스트 분해
no_list = sum(no_app, [])
title_list = sum(title_app, [])
nick_list = sum(nick_app, [])
like_list = sum(like_app, [])



# 판다스화
df = pd.DataFrame({'번호':no_list,
                   '제목':title_list,
                   '작성자':nick_list,
                   '좋아요':like_list})
# 필독, 공지 삭제
df = df.drop(df[df['번호'] == '필독'].index)
df = df.drop(df[df['번호'] == '공지'].index)
df = df.reset_index(drop=True)

print('글 ', len(df), '개 크롤링 완료. \n크롤링 종료.', sep='')


# 저장
df.to_excel('crawler_naver cafe_게시판 {}.xlsx'.format(keyword))