# import library
from bs4 import BeautifulSoup
import pymongo
import requests
import re


# mongodb connection
def mongodb_connect():
    conn = pymongo.MongoClient()
    actor_db = conn.cine21
    actor_collection = actor_db.actor_collection


# 배우 상세정보 가져오기
def get_actor_details(link):
    try:
        res = requests.get(link)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            default_info = soup.select_one('ul.default_info')
            actor_details = default_info.select('li')
            for actor_item in actor_details:
                print(actor_item)
                print(actor_item.select_one('span.tit').get_text())
                actor_item_value = re.sub(
                    '<span.*?>.*?</span>', '', str(actor_item))    # https://regexr.com/
                actor_item_value = re.sub('<.*?>', '', actor_item_value)
                print(actor_item_value)

            print()
    except:
        pass


# 크롤링 주소 requests
def requests_cine21():
    cine21_url = 'http://www.cine21.com/rank/person/content'
    post_data = dict()
    post_data['section'] = 'actor'
    post_data['period_start'] = '2020-02'
    post_data['gender'] = 'all'
    post_data['page'] = 1
    try:
        res = requests.post(cine21_url, data=post_data)

        # parsing과 데이터 추출
        if res.status_code == 200:
            soup = BeautifulSoup(res.content, 'html.parser')
            # 배우 이름 추출
            actors = soup.select('li.people_li div.name')
            for actor in actors:
                if actor.get_text() != None:
                    actor_name = re.sub('\(\w*\)', '', actor.get_text())
            # 배우 상세정보 추출
            for actor in actors:
                actor_link = 'http://www.cine21.com' + \
                    actor.select_one('a')['href']
                get_actor_details(actor_link)
    except:
        pass


def main():
    mongodb_connect()
    requests_cine21()


main()
