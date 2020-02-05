# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from os.path import join, dirname
from flask import Flask, request, redirect, url_for, session, flash
from application.index import *
app = Flask(__name__, static_folder='../ui/static', template_folder='../ui/templates')
app.secret_key = 'linear_programming_problem'


@app.route('/',  methods=["GET", "POST"])
def index():
    return show()


if __name__ == '__main__':
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    env = os.environ.get("name")
    if env == "production":
        app.config["ENV"] = "production"
        app.run(host='0.0.0.0', port='3300')
    else:
        app.config["ENV"] = "development"
        app.debug = True
        app.run(host='0.0.0.0', port='3000')
