# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import selenium.webdriver.support.ui as UI
import re


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument('--disable-gpu')

# selenium의 path
# 사용자 마다 경로가 다르므로 lib directory에 selenium chromedriver 추가하여 이용
path = "../lib/chromedriver.exe"
# 크롤링 하려는 페이지의 URL
url = 'http://www.coupang.com/np/categories/388046?eventCategory=breadcrumb&eventLabel=&page='

# driver = webdriver.Chrome(executable_path = path, chrome_options = options)
driver = webdriver.Chrome(executable_path = path)
wait = UI.WebDriverWait(driver, 10)


# Jquery 실행의 반응을 기다리는 함수
def ajax_complete(dv):
    try:
        return 0 == dv.execute_script("return jQuery.active")
    except WebDriverException:
        pass


# 크롤링한 텍스트 중 쓸모없는 부분을 삭제
def pre_processing(input_str):
    result = re.sub('<div class="sdp-review__article__list__review__content js_reviewArticleContent">', '', input_str)
    result = re.sub('\n+\s*', '', result)
    result = re.sub(r'[\s]*</div>', '', result)
    result = re.sub(r'<br/>', '', result)
    result += "\n------------------------------------------------\n"

    return result


# 크롤링 하는 함수
def crawler(page_num):
    driver.get(url + str(page_num))

    # 리뷰 컨테이너 클릭
    elems = driver.find_elements_by_class_name('baby-product')
    size = len(elems)
    print("page num :", page_num)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 크롤링할 리뷰의 수
    product_list = eval(soup.find("ul", id="productList")["data-products"])['indexes']

    # 리뷰의 수 만큼 크롤링
    for i in range(size):
        output_file = "./reviews_01/review_" + str(page_num).zfill(2) + "_" + str(i).zfill(4) + "_" + str(product_list[i]) + ".txt"

        print("start crawling : " + str(page_num).zfill(2) + "_" + str(i).zfill(4) + "_" + str(product_list[i]))

        elems[i].click()
        driver.implicitly_wait(3)

        # 리뷰 컨테이너 클릭
        elem = driver.find_element_by_name('review')

        review = []

        count = 0
        while len(review) is 0:
            elem.click()
            review = driver.find_elements_by_class_name("sdp-review__article__page__num")
            driver.implicitly_wait(3)
            count += 1
            if count is 5:
                break
        if count is 5:
            driver.get(url + str(page_num))
            driver.implicitly_wait(3)
            try:
                elems = driver.find_elements_by_class_name('baby-product')
                driver.implicitly_wait(3)
            except WebDriverException:
                print("Alert error")
                Alert(driver).accept()

                elems = driver.find_elements_by_class_name('baby-product')
                driver.implicitly_wait(3)
            print(">> no review")
            print("end crawling : " + str(page_num).zfill(2) + "_" + str(i).zfill(4) + "_" + str(product_list[i]))
            print("----------------------------------------------------------------------------")
        else:
            # 전체 페이지 가져오기
            temp = driver.find_element_by_class_name("sdp-review__average__total-star__info-count").text.split(",")

            # ,가 있으면 길이가 두개 없으면 한개
            if len(temp) is 1:
                temp2 = temp[0]
            else:
                temp2 = temp[0] + temp[1]

            if int(int(temp2) % 50) is 0:
                total_page = int(int(temp2) / 50)
            else:
                total_page = int(int(temp2) / 50) + 1

            if int(int(temp2) % 5) is 0:
                end_index = int(int(temp2) / 5)
            else:
                end_index = int(int(temp2) / 5) + 1

            print(">> total review :", temp2)
            print(">> total page :", end_index)

            temp = driver.find_element_by_class_name("sdp-review__article__page")
            data_start = int(temp.get_attribute("data-start"))
            data_end = int(temp.get_attribute("data-end"))

            open_result_file = open(output_file, 'a', encoding='UTF-8', newline='')

            index = 0
            for k in range(1, total_page + 1):
                for u in range(data_start, data_end + 1):
                    if index is int(end_index * 1 / 4) and index is not 0:
                        print(">> 25% :", index)
                    elif index is int(end_index * 2 / 4):
                        print(">> 50% :", index)
                    elif index is int(end_index * 3 / 4):
                        print(">> 75% :", index)

                    index += 1

                    try:
                        next_page = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-page=' + str(u) + ']')))
                        next_page.click()
                        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")

                        # 여기 부터 크롤링
                        # notice에 한페이지에 있는 모든 리뷰(5개)를 저장
                        html = driver.page_source
                        soup = BeautifulSoup(html, 'html.parser')
                        notice = soup.find_all('div',
                                               {"class": "sdp-review__article__list__review__content js_reviewArticleContent"})
                        driver.implicitly_wait(5)

                        result_text = ""
                        for j in range(len(notice)):
                            result_text += pre_processing(str(notice[j]))

                        open_result_file.write(result_text)
                    except Exception:
                        print("error : one page")

                if data_end < end_index:
                    try:
                        next_btn = wait.until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'sdp-review__article__page__next')))
                        next_btn.click()
                        WebDriverWait(driver, 10).until(ajax_complete, "Timeout waiting for page to load")

                        temp = driver.find_element_by_class_name("sdp-review__article__page")
                        data_start = int(temp.get_attribute("data-start"))
                        data_end = int(temp.get_attribute("data-end"))
                    except Exception:
                        open_result_file.close()
                        break
                else:
                    open_result_file.close()

            driver.get(url + str(page_num))
            driver.implicitly_wait(3)
            try:
                elems = driver.find_elements_by_class_name('baby-product')
                driver.implicitly_wait(3)
            except WebDriverException:
                print("Alert error")
                Alert(driver).accept()

                elems = driver.find_elements_by_class_name('baby-product')
                driver.implicitly_wait(3)
            print("end crawling : " + str(page_num).zfill(2) + "_" + str(i).zfill(4) + "_" + str(product_list[i]))
            print("----------------------------------------------------------------------------")


for i in range(3, 18):
    crawler(i)
