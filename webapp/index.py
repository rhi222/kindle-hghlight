#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template
import os
import json


app = Flask(__name__)


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


@app.route('/hello')
def hello():
    name = "Hello World"
    return name


@app.route('/api/json')
def api_json():
    response = jsonify(get_kindle_data())
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run(debug=True)
