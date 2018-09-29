#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import slackweb
import os
import json
# from pprint import pprint
import random

# todo
# - [ ] blacklist
# - [ ] whitelist
# - [x] random

# 表示するハイライトの情報数
display_highilight_number = 3


def get_kindle_data():
    json_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../data-generator",
            "kindle.json"
    )
    with open(json_path) as f:
        data = json.load(f)
    return data


def get_random_number(max_number):
    '''
    0 <= N <= max と整数をランダムで返却
    '''
    return random.randrange(0, max_number)


def targetting_book_info(data):
    '''
    出力対象の書籍の情報取得
    '''
    asin_list = data.keys()  # ie: amazon_standard_identification_number
    target_asin_idx = get_random_number(len(asin_list) - 1)
    target_asin = asin_list[target_asin_idx]
    target_book = data[target_asin]
    return target_book


def get_highilights_info(highlights, display_highilight_number):
    '''
    出力対象のハイライト箇所の情報取得
    '''
    return random.sample(highlights, display_highilight_number)


def create_message(post_info):
    message = '''
    ■ {book_title}
    '''.format(
        book_title=post_info['book']['title']
    )
    return message


if __name__ == '__main__':
    data = get_kindle_data()
    target_book = targetting_book_info(data)
    highlights = get_highilights_info(
        target_book['highlights'],
        display_highilight_number
    )
    post_info = {
        'book': target_book,
        'highlights': highlights
    }
    slack_message = create_message(post_info)
    print(slack_message)
