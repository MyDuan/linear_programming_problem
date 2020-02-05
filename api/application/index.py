from flask import render_template, session


def show():
    return render_template('index.html')
