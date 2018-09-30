#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, send_from_directory
import os
import sys
import json
sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '../slack-messenger'
    )
)
from post_slack import get_target_book_info  # noqa E402

app = Flask(__name__, static_url_path='')
app.config["CACHE_TYPE"] = "null"


def get_kindle_data():
    json_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../data-generator",
            "kindle.json"
    )
    with open(json_path) as f:
        data = json.loads(f.read(), 'utf-8')
    return data


@app.route('/')
def root_url():
    return render_template('index.html')


@app.route('/build/<path:path>')
def send_js(path):
    return send_from_directory('build', path)


@app.route('/hello')
def hello():
    name = "Hello World"
    return name


@app.route('/api/json/all')
def api_json():
    print('---- json all')
    response = jsonify(get_kindle_data())
    response.status_code = 200
    return response


@app.route('/api/json/book')
def book_json():
    print('---- json book')
    book_data = get_target_book_info(get_kindle_data())
    response = jsonify(book_data)
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True)
