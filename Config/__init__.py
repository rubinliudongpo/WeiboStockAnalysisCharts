# -*- coding: utf-8 -*-
DEFAULT_WEIBO_ID = ''
LOGIN_URL = 'https://passport.weibo.cn/signin/login'

# change this to your PhantomJS executable file, full path
PHANTOM_JS_PATH = '/usr/bin/phantomjs'

COOKIES_SAVE_PATH = 'Config/Cookies.pkl'

accounts = [
    {
        "id": '',
        "password": '',
    },
]

DB_HOST = "localhost"
DB_PORT = 3306
DB_USER = ""
DB_PASSWD = ""
DB_NAME = ""
DB_CHARSET = "utf8"

STOCK_INSERT_SQL = "insert into stock_recommendations(weibo_id, publish_time_stamp, " \
                   "stock_id, stock_comment_ahead, stock_comment_rear, created_at) " \
                   "values(%s, %s, %s, %s, %s, %s)"

STOCK_SEARCH_SQL = "SELECT * FROM stock_recommendations where weibo_id = %s " \
             "and stock_id = %s and stock_comment_ahead = %s and stock_comment_rear= %s"
