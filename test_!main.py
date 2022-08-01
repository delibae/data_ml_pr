
import sys    
import os     

import pandas as pd    
import numpy as np     

from bs4 import BeautifulSoup     
from selenium import webdriver    
from selenium.webdriver.common.keys import Keys

import time                      
import math

# 게시판 이름 입력
keyword = "동물병원 질문과 정보♡"

# 크롤링 할 글 입력
crawling_no = 200

# 크롬 웹브라우저 실행
driver = webdriver.Chrome("E:\python\data_collect\data_ml_pr\chromedriver.exe")

# 네이버 일회용 로그인
driver.get("https://nid.naver.com/nidlogin.login?url=http://section.cafe.naver.com")
time.sleep(1)


driver.find_element_by_id("ones").click()
user_id = driver.find_element_by_id("disposable")

#일회용 로그인 입력
user_id.send_keys("41623004")
driver.find_element_by_id("otnlog.login").click()
time.sleep(2)

# 사이트 주소 입력
driver.get("https://cafe.naver.com/healingdogcat")
time.sleep(2)

# 게시판 클릭
driver.find_element_by_link_text(keyword).click()


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
href_app = []


# 크롤링 해야 할 페이지 계산
crawling_page = int(math.ceil(crawling_no / 50)+1)


try: 

    for page in range(1,crawling_page):
        # 페이지 클릭
        driver.find_element_by_link_text(str(page)).click()
        time.sleep(1)
        # 글 번호 수집
        no = [i.text for i in driver.find_elements_by_css_selector('.td_article')]
        no_split = [ni.split()[0] for ni in no]
        # 글 제목 수집
        title = [i.text for i in driver.find_elements_by_css_selector('.article')]
        # 글 링크 수집
        href = [i.get_attribute('href') for i in driver.find_elements_by_css_selector('.article')]
        # 작성자 수집
        nick = [i.text for i in driver.find_elements_by_css_selector('.p-nick .m-tcol-c')]
        # 좋아요 수집
        like = [i.text for i in driver.find_elements_by_css_selector('.td_likes')]
        # 수집 데이터 append
        no_app.append(no_split)
        title_app.append(title)
        nick_app.append(nick)
        like_app.append(like)

        href_app.append(href)
        # 10페이지 마다 프린트 & 다음 페이지로 클릭
        if str(page)[-1] == '0':
            print(int(page), 'page 크롤링 완료')
            driver.find_element_by_link_text('다음').click()
# 더이상 페이지가 존재하지 않을 시
except:
    print('더이상 페이지가 존재하지 않음'*10)

# 리스트안 리스트 분해
no_list = sum(no_app, [])
title_list = sum(title_app, [])
nick_list = sum(nick_app, [])
like_list = sum(like_app, [])
href_list = sum(href_app,[])

#공지 없애기 입력
notifi_len = 15
no_list = no_list[notifi_len:]
title_list = title_list[notifi_len:]
nick_list = nick_list[notifi_len:]
like_list = like_list[notifi_len:]
href_list = href_list[notifi_len:]

print(href_list)

res_list = []
count = 0
for link in href_list:
    count += 1
    print(count)
    try:
        driver.get(link)
        time.sleep(3)
        driver.switch_to.frame("cafe_main")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # 게시글에서 제목 추출
        # title = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_header > div.ArticleTitle > div > h3').get_text()

        # 내용을 하나의 텍스트로 만든다. (띄어쓰기 단위)
        try:
            content_tags = soup.select_one('#app > div > div > div.ArticleContentBox > div.article_container > div.article_viewer').select('p')
            content_tags = [ tags.get_text() for tags in content_tags ]

        except:
            content_tags = ''
            print("error1")
    except:
        content_tags = ''
        print("error2")

    de_list = []
    if content_tags != '':
        for i in range(len(content_tags)):
            if content_tags[i].find('■') != -1 or content_tags[i].find('☆') != -1 or content_tags[i].find('──────────────────') != -1:
                print("범인은 너!")
                print(content_tags[i])
                de_list.append(i)
                print("사라져버려!")
    de_list.sort(reverse=True)
    for i in de_list:
        del content_tags[i]
    content = ' '.join(content_tags)
    # dict형태로 만들어 결과 list에 저장
    # res_list.append({'title' : title, 'content' : content})
    res_list.append(content)

driver.close()

# 판다스화
df = pd.DataFrame({'번호':no_list,
                   '제목':title_list,
                   '작성자':nick_list,
                   '좋아요':like_list,
                   '링크':href_list,
                   '글내용':res_list})
# 필독, 공지, 빈 글 내용 삭제
df = df.drop(df[df['번호'] == '필독'].index)
df = df.drop(df[df['번호'] == '공지'].index)
df = df.drop(df[df['글내용'] == ''].index)
df = df.reset_index(drop=True)

print('글 ', len(df), '개 크롤링 완료. \n크롤링 종료.', sep='')


# 저장
df.to_excel('crawler_naver cafe_게시판 {}.xlsx'.format(keyword))