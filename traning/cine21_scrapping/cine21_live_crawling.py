# import library
from bs4 import BeautifulSoup
import pymongo
import requests
import re


# mongodb connection and insert data
def mongodb_connect(insert_data):
    conn = pymongo.MongoClient()
    actor_db = conn.cine21
    actor_collection = actor_db.actor_collection
    actor_collection.insert_many(insert_data)


# 배우 상세정보 가져오기
def get_actor_details(link):
    try:
        res = requests.get(link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            default_info = soup.select_one('ul.default_info')
            actor_details = default_info.select('li')

            actor_info_dict = dict()

            for actor_item in actor_details:
                actor_item_field = actor_item.select_one('span.tit').get_text()
                actor_item_value = re.sub(
                    '<span.*?>.*?</span>', '', str(actor_item))    # https://regexr.com/
                actor_item_value = re.sub(
                    '<.*?>', '', actor_item_value)    # 정규 표현식 3분 참조
                actor_info_dict[actor_item_field] = actor_item_value
            return actor_info_dict
    except:
        pass


# 각 페이지 크롤링
def get_cine21_page(cine21_url, post_data, actors_info_list, index):
    post_data['page'] = index
    try:
        res = requests.post(cine21_url, data=post_data)

        # parsing과 데이터 추출
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')

            # 배우 랭킹, 상세정보, 배우이름, 흥행지수, 출연영화 추출
            actors = soup.select('li.people_li div.name')
            hits = soup.select('ul.num_info > li > strong')
            movies = soup.select('ul.mov_list')
            rankings = soup.select('li.people_li span.grade')
            for index, actor in enumerate(actors):
                # 배우 랭킹 추출
                ranking = int(rankings[index].get_text())    # 배우 랭킹정보

                # 배우 상세정보 추출
                actor_link = 'http://www.cine21.com' + \
                    actor.select_one('a')['href']
                actor_info_dict = get_actor_details(actor_link)    # 배우 상세정보

                if actor.get_text() != None:
                    # 배우 이름 추출
                    actor_name = re.sub('\(\w*\)', '', actor.get_text())

                    # 흥행 지수 추출
                    actor_hits = int(hits[index].get_text().replace(',', ''))

                    # 출연 영화 추출
                    movie_titles = movies[index].select('li a span')
                    movie_title_list = list()
                    for movie_title in movie_titles:
                        movie_title_list.append(movie_title.get_text())

                    actor_info_dict['배우이름'] = actor_name
                    actor_info_dict['흥행지수'] = actor_hits
                    actor_info_dict['출연영화'] = movie_title_list
                    actor_info_dict['랭킹'] = ranking

                actors_info_list.append(actor_info_dict)

    except:
        pass


# cine21 전체 페이지 크롤링, db에 담을 list에 데이터 삽입
def get_pages_and_save_list():
    cine21_url = 'http://www.cine21.com/rank/person/content'
    post_data = dict()
    post_data['section'] = 'actor'
    post_data['period_start'] = '2020-02'
    post_data['gender'] = 'all'
    post_data['page'] = 1
    try:
        res = requests.post(cine21_url, data=post_data)
        soup = BeautifulSoup(res.content, 'html.parser')

        pagenation = soup.select_one('div.pagination')
        last_page_num = pagenation.select_one('.btn_end').attrs['href']
        last_page_num = int(
            re.sub('\w.*\(', '', last_page_num).split(')')[0])    # 마지막 페이지

        actors_info_list = list()    # db에 push할 배우 정보들을 담을 리스트

        for i in range(last_page_num):
            print(f"{i + 1} page in progress...")
            get_cine21_page(cine21_url, post_data, actors_info_list, i + 1)

        mongodb_connect(actors_info_list)
    except:
        pass


def main():
    get_pages_and_save_list()
