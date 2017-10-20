# -*- coding: utf-8 -*-
import argparse

from WeiboData.Core.Dispatcher import Dispatcher
from Config import DEFAULT_WEIBO_ID


def parse_args():
    parser = argparse.ArgumentParser(description='WeiboStockAnalysis. Rubin Liu')

    _help_ = 'set Weibo id.'
    parser.add_argument('-i', '--id', default=DEFAULT_WEIBO_ID, help=_help_)

    _help_ = 'set weibo filter flag:' \
             'if filter is 0, then weibos are all original;' \
             'if 1, it will contain re-post weibos. default is 0.'
    parser.add_argument('-f', '--filter', default='1', help=_help_)

    _help_ = 'set update weibo cookie:' \
             'set 1 to enable updating cookie' \
             'set 0 to disable updating cookies.'
    parser.add_argument('-u', '--update_cookies', default='0', help=_help_)

    _args_ = parser.parse_args()
    return _args_


if __name__ == '__main__':
    args = parse_args()

    filter_flag = False
    if args.filter:
        filter_flag = True if args.filter == "1" else False

    update_cookies = False
    if args.update_cookies:
        update_cookies = True if args.update_cookies == "1" else False

    uid = args.id
    if uid:
        dispatcher = Dispatcher(uid=uid, filter_flag=filter_flag, update_cookies=update_cookies)
        dispatcher.execute()
    else:
        print('please add weibo uid here.')

