from flask import render_template, session


def show(data):
    if session.get('results'):
        if data:
            return render_template('index.html', results=session['results'], data=data)
        else:
            return render_template('index.html', results=session['results'])
    else:
        if data:
            return render_template('index.html', data=data)
        else:
            return render_template('index.html')
