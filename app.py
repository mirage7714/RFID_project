# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request, render_template, send_from_directory, redirect, url_for, session
import json
from datetime import datetime
import sqlite3
import requests
from bookParser import parseBookData
import pandas as pd
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy

import json

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config["SECRET_KEY"] = "abc"
db = SQLAlchemy()


# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    permission = db.Column(db.Integer)


login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


def get_all_users():
    user_list = []
    all_users = Users.query.all()
    for user in all_users:
        user_list.append({
            'username': user.username,
            'permission': user.permission,
            'id': user.id
        })
    return user_list


def updateHistory(result):
    index = len(json.loads(requests.get(history_url).text)) + 1
    history_payload = {}
    data = []
    data.append({
        'No': index,
        'ISBN': result[0]['ISBN'],
        'Name': result[0]['Name'],
        'Date': datetime.strftime(datetime.now(), '%Y/%m/%d')
    })
    history_payload['data'] = data
    requests.post(  history_url, json=history_payload)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                     password=request.form.get("password"),
                     permission=99
                     )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        if user.password == request.form.get("password"):
            login_user(user)
            session['username'] = user
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/')
def home():
    # return render_template('login.html')
    return redirect(url_for('login'))


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/query_book', methods=['POST'])
def query():
    user = request.form.get('user')
    url = f'http://localhost:8000/users/{user}'
    response = json.loads(requests.get(url).text)
    result = [{
        'email': response['email'],
        'password': response['password'],
        'id': response['id'],
        'name': response['name']
    }]
    return render_template('book.html', user=user, results=result)


@app.route('/history')
def history():
    url = 'http://localhost:8000/users/'
    response = json.loads(requests.get(url).text)
    result = []
    for q in response:
        result.append({
            'email': q['email'],
            'password': q['password'],
            'id': q['id'],
            'name': q['name']
        })
    return render_template('history.html', results=result)


@app.route('/statistics')
def personal_page():
    result = get_all_users()
    return render_template('statistics.html', results=result)


@app.route('/reset')
def reset():
    return render_template('reset.html', result=[])


if __name__ == "__main__":
    app.run(port=5000, debug=True)
