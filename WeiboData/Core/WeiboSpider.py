# -*- coding: utf-8 -*-
"""
using guide:
setting accounts first:

under: weibo_terminator/settings/accounts.py
you can set more than one accounts, WT will using all accounts one by one,
if one banned, another will move on.

if you care about security, using subsidiary accounts instead.

"""
import re
import time
import requests
from lxml import etree
from Config import COOKIES_SAVE_PATH, DB_HOST, DB_PORT, DB_USER, DB_PASSWD, DB_NAME, \
    DB_CHARSET, STOCK_INSERT_SQL, STOCK_SEARCH_SQL
import pickle
import pymysql
from WeiboData.Utilities.Utilities import encode_publish_time, is_number


class WeiboSpider(object):

    def __init__(self, using_account, uuid, start_date, end_date, filter_flag=False):
        self.using_account = using_account
        self.connection = None
        self._init_cookies()
        self._init_headers()
        self._init_db()

        self.user_id = uuid
        self.start_date = start_date
        self.end_date = end_date
        self.filter = filter_flag
        self.weibo_scraped = 0
        self.weibo_detail_urls = []
        self.stock_recommendations = []
        self.stock_comments = []

    def _init_cookies(self):
        try:
            with open(COOKIES_SAVE_PATH, 'rb') as f:
                cookies_dict = pickle.load(f)
            cookies_string = cookies_dict[self.using_account]
            cookie = {
                "Cookie": cookies_string
            }
            print('setting cookies..')
            self.cookie = cookie
        except FileNotFoundError:
            print('have not get cookies yet.')

    def _init_headers(self):
        headers = requests.utils.default_headers()
        user_agent = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko/20100101 Firefox/11.0'
        }
        headers.update(user_agent)
        print('headers: ', headers)
        self.headers = headers

    def _init_db(self):
        self.connection = pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER,
                                          passwd=DB_PASSWD, db=DB_NAME, charset=DB_CHARSET)

    def crawl(self):
        try:
            self._get_html()
            self._get_stock_weibos()
            print('-' * 30)
            return True
        except Exception as e:
            print(e)
            print('Error:it seems something wrong with current account, please check it')
            return False

    def _get_html(self):
        try:
            if is_number(self.user_id):
                url = 'http://weibo.cn/u/%s?filter=%s&page=1' % (self.user_id, self.filter)
                print(url)
            else:
                url = 'http://weibo.cn/%s?filter=%s&page=1' % (self.user_id.format("utf-8"), self.filter)
                print(url)
            self.html = requests.get(url, cookies=self.cookie, headers=self.headers).content
        except Exception as e:
            print(e)

    def _get_stock_weibos(self):
        print('-- getting stock weibos')
        selector = etree.HTML(self.html)

        try:
            if selector.xpath('//input[@name="mp"]') is None:
                page_num = 1
            else:
                page_num = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            # pattern = r"\d+\.?\d*"
            print('--- all weibo page {}'.format(page_num))

            try:
                for page in range(1, page_num):
                    url2 = 'http://weibo.cn/%s?filter=%s&page=%s' % (self.user_id, self.filter, page)
                    html2 = requests.get(url2, cookies=self.cookie, headers=self.headers).content
                    selector2 = etree.HTML(html2)
                    info = selector2.xpath("//div[@class='c']")
                    print('---- current solving page {}'.format(page))

                    if page % 10 == 0:
                        print('take a nap for 5 minutes to cheat weibo site to avoid account baning.')
                        time.sleep(60*5)

                    if len(info) > 3:
                        for i in range(0, len(info) - 2):
                            temp_list = [self.user_id]
                            detail = info[i].xpath("@id")[0]
                            self.weibo_detail_urls.append('http://weibo.cn/comment/{}?uid={}&rl=0'.
                                                          format(detail.split('_')[-1], self.user_id))

                            self.weibo_scraped += 1
                            str_t = info[i].xpath("div/span[@class='ctt']")
                            weibos = str_t[0].xpath('string(.)')
                            time_t = info[i].xpath("div/span[@class='ct']")
                            publish_time = time_t[0].xpath('string(.)')
                            print(publish_time)
                            time_stamp = encode_publish_time(publish_time)
                            if self.start_date > time_stamp:
                                print("self.start_date > time_stamp")
                                return
                            temp_list.append(str(time_stamp))

                            stock_recommendation_id_pattern = re.compile("#[\u4e00-\u9fa5]{3,}\s(s[h|z]\d{6})\[股票\]#")
                            stock_recommendation_id = stock_recommendation_id_pattern.search(weibos)
                            if stock_recommendation_id:
                                temp_list.append(stock_recommendation_id.group(1))
                                stock_comment_ahead_pattern = re.compile("(.*)#[\u4e00-\u9fa5]{3,}\ss[h|z]\d{6}\[股票\]#")
                                stock_comment_ahead = stock_comment_ahead_pattern.search(weibos)
                                if stock_comment_ahead:
                                    temp_list.append(stock_comment_ahead.group(1).replace(u"\u200b", "").
                                                     replace(u"\xa0", "").lstrip().rstrip().lstrip("\n").rstrip("\n"))
                                stock_comment_rear_pattern = re.compile("#[\u4e00-\u9fa5]{3,}\ss[h|z]\d{6}\[股票\]#(.*)")
                                stock_comment_rear = stock_comment_rear_pattern.search(weibos)
                                if stock_comment_rear:
                                    temp_list.append(stock_comment_rear.group(1).replace(u"\u200b", "").
                                                     replace(u"\xa0", "").lstrip().rstrip().lstrip("\n").rstrip("\n"))
                                print(temp_list)
                                temp_list.append(str(int(time.time())))
                                with self.connection.cursor() as cursor:
                                    cursor.execute(STOCK_SEARCH_SQL, [temp_list[0], temp_list[2], temp_list[3], temp_list[4]])
                                    search_result = cursor.fetchall()
                                    if len(search_result) == 0:
                                        try:
                                            cursor.execute(STOCK_INSERT_SQL, temp_list)
                                            self.connection.commit()
                                        except:
                                            self.connection.rollback()

            except etree.XMLSyntaxError as e:
                print('get weibo info finished.')
        except IndexError as e:
            print(e)
            print('get weibo info done, current user {} has no weibo yet.'.format(self.user_id))
        finally:
            self.connection.close()


