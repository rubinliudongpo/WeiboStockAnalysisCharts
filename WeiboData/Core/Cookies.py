# -*- coding: utf-8 -*-

import os
from selenium import webdriver
from selenium.common.exceptions import InvalidElementStateException
import time
from tqdm import *
import pickle
from Config import LOGIN_URL, PHANTOM_JS_PATH, COOKIES_SAVE_PATH


def count_time():
    for i in tqdm(range(40)):
        time.sleep(0.5)


def get_cookie_from_network(account_id, account_password):
    phantom_js_driver_file = os.path.abspath(PHANTOM_JS_PATH)
    if os.path.exists(phantom_js_driver_file):
        driver = webdriver.PhantomJS(phantom_js_driver_file)
        try:
            # you must set window size here, otherwise it will not return elements to you
            driver.set_window_size(1640, 688)
            driver.get(LOGIN_URL)
            # before get element sleep for 4 seconds, waiting for page render complete.
            count_time()
            driver.find_element_by_xpath('//input[@id="loginName"]').send_keys(account_id)
            driver.find_element_by_xpath('//input[@id="loginPassword"]').send_keys(account_password)
            # print('account id: {}'.format(account_id))
            # print('account password: {}'.format(account_password))
            driver.find_element_by_xpath('//a[@id="loginAction"]').click()
        except InvalidElementStateException as e:
            print(e)
            print('Error:invalid account id or password {}, please update it\n'.format(account_id))

        try:
            cookie_list = driver.get_cookies()
            cookie_string = ''
            for cookie in cookie_list:
                if 'name' in cookie and 'value' in cookie:
                    cookie_string += cookie['name'] + '=' + cookie['value'] + ';'
            if 'SSOLoginState' in cookie_string:
                print('Success getting cookies!! \n {}'.format(cookie_string))
                if os.path.exists(COOKIES_SAVE_PATH):
                    with open(COOKIES_SAVE_PATH, 'rb') as f:
                        cookies_dict = pickle.load(f)
                    if cookies_dict[account_id]:
                        cookies_dict[account_id] = cookie_string
                        with open(COOKIES_SAVE_PATH, 'wb') as f:
                            pickle.dump(cookies_dict, f)
                        print('Successfully saving cookies into {}. \n'.format(COOKIES_SAVE_PATH))
                else:
                    cookies_dict = dict()
                    cookies_dict[account_id] = cookie_string
                    with open(COOKIES_SAVE_PATH, 'wb') as f:
                        pickle.dump(cookies_dict, f)
                    print('Successfully save cookies into {}. \n'.format(COOKIES_SAVE_PATH))
                return cookie_string
            else:
                print('Error:invalid account id or password {}, please update it\n'.format(account_id))
        except Exception as e:
            print(e)
    else:
        print('Error:fail to find PhantomJS driver, please download it from '
              'http://phantomjs.org/download.html.')
