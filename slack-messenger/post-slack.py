#!/usr/bin/env python
# -*- coding: utf-8 -*-
import slackweb
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
slack_conf = {
    "webhook_url": 'https://hooks.slack.com/services/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',  # noqa: E501
    "channel": "#zzz_nishiyama_test",
    "username": "jira_bot",
    "icon": ":jira2:"
}


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
    '''
    slackに投稿する文字列を生成
    '''
    highlights_message = '\n'.join(map(
        # lambda h: "- {text}".format(text=h['text'].encode('utf-8')),
        lambda h: "- <{deep_link}|{text}>".format(
            text="{text} | location:{location}".format(
                text=h['text'].encode('utf-8'),
                location=h['location'].encode('utf-8'),
            ),
            deep_link="kindle://book?action=open&asin={asin}&location={location}"  # noqa: E501
                .format(
                    asin=post_info['book']['asin'],
                    location=h['location'],
                )
        ),
        post_info['highlights']
    ))
    message = '''
    ■ {book_title} | {author}
    {highlights_message}
    '''.format(
        book_title=post_info['book']['title'].encode('utf-8'),
        author=post_info['book']['author'].encode('utf-8'),
        highlights_message=highlights_message
    )
    return message


# todo: logic切り出し
def create_highlight_message(highlight, book_info):
    return


def post_slack(slack_messeage, slack_conf):
    '''
    confファイルで指定された内容でslackに投稿
    '''
    slack = slackweb.Slack(url=slack_conf["webhook_url"])
    slack.notify(
        channel=slack_conf["channel"],
        username=slack_conf["username"],
        text=slack_messeage,
        icon_emoji=slack_conf["icon"]
    )
    return


def get_target_book_info(data):
    target_book = targetting_book_info(data)
    highlights = get_highilights_info(
        target_book['highlights'],
        display_highilight_number
    )
    post_info = {
        'book': target_book,
        'highlights': highlights
    }
    return post_info


if __name__ == '__main__':
    data = get_kindle_data()
    post_info = get_target_book_info(data)
    slack_messeage = create_message(post_info)
    post_slack(slack_messeage, slack_conf)
