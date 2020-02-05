# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
from os.path import join, dirname
from flask import Flask, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from application.index import *
from models import *
app = Flask(__name__, static_folder='../ui/static', template_folder='../ui/templates')
app.secret_key = 'linear_programming_problem'
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please login.'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    if query_user(user_id) is not None:
        curr_user = User()
        curr_user.id = user_id

        return curr_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user_id = request.form.get('userid')
        user = query_user(user_id)
        if user is not None and request.form['password'] == user['password']:

            curr_user = User()
            curr_user.id = user_id

            login_user(curr_user)

            return redirect(url_for('index'))

        flash('Wrong username or password!')

    return render_template('login.html', title="Sign In")


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/',  methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    return show()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


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
