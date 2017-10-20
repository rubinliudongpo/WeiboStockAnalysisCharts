# -*- coding: utf-8 -*-
from WeiboData.Core.WeiboSpider import WeiboSpider
from Config import COOKIES_SAVE_PATH
from Config import accounts
import os
from WeiboData.Core.Cookies import get_cookie_from_network
import pickle


class Dispatcher(object):
    """
    Dispatcher, if your cookies is out of date, set update_cookies to True to
    update all accounts cookies
    """
    def __init__(self, uid, filter_flag=False, update_cookies=False):
        self.filter_flag = filter_flag
        self.update_cookies = update_cookies
        self._init_accounts_cookies()
        self._init_accounts()
        self.user_id = uid

    def execute(self):
        self._execute()

    def _init_accounts_cookies(self):
        """
        get all cookies for accounts, dump into pkl, this will only run once, if
        you update accounts, set update to True
        :return:
        """
        if self.update_cookies:
            for account in accounts:
                print('preparing cookies for account {}'.format(account))
                get_cookie_from_network(account['id'], account['password'])
            print('getting cookies for all accounts, and start weibo crawling ...')
        else:
            if os.path.exists(COOKIES_SAVE_PATH):
                pass
            else:
                for account in accounts:
                    print('preparing cookies for account {}'.format(account))
                    get_cookie_from_network(account['id'], account['password'])
                print('getting cookies for all accounts, and start weibo crawling ...')

    def _init_accounts(self):
        """
        setting accounts
        :return:
        """
        try:
            with open(COOKIES_SAVE_PATH, 'rb') as f:
                cookies_dict = pickle.load(f)
            self.all_accounts = list(cookies_dict.keys())
            print('----------- detected {} accounts, weibo_terminator will using all accounts to scrap '
                  'automatically -------------'.format(len(self.all_accounts)))
            print('detected accounts: ', self.all_accounts)
        except Exception as e:
            print(e)
            print('error:no cookies file.')
      
    def _execute(self):
        scraper = WeiboSpider(using_account=self.all_accounts[0], uuid=self.user_id, filter_flag=self.filter_flag)
        i = 1
        while True:
            result = scraper.crawl()
            if result:
                print('finished!!!')
                break

    def _init_multi_mode(self):
        pass


