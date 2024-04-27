# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from flask import Flask, request, render_template, redirect, url_for, session, jsonify
import requests
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import pandas as pd
import os
import json

app = Flask(__name__)
app.static_folder = 'static'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../traffic.db'
app.config["SECRET_KEY"] = os.urandom(16).hex()
db = SQLAlchemy()


#Reading data
data_df = pd.read_csv("static/data/Churn_data.csv")
churn_df = data_df[(data_df['Churn'] == "Yes").notnull()]


# Create user model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    permission = db.Column(db.Integer)


class Data(db.Model):
    __tablename__ = 'data'
    time = db.Column(db.String, primary_key=True)
    section_id = db.Column(db.String(250), primary_key=True)
    section_name = db.Column(db.String(250))
    avg_speed = db.Column(db.Float)
    avg_occ = db.Column(db.Float)
    total_vol = db.Column(db.Float)

    def __init__(self, time, section_id, section_name, avg_speed, avg_occ, total_vol):
        self.time = time
        self.section_id = section_id
        self.section_name = section_name
        self.avg_speed = avg_speed
        self.avg_occ = avg_occ
        self.total_vol = total_vol


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.init_app(app)
with app.app_context():
    db.create_all()


# Creates a user loader callback that returns the user object given an id
@login_manager.user_loader
def loader_user(username):
    user = Users.query.get(username)
    if not user:
        return
    return user


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


@app.route('/delete/<username>', methods=['POST'])
def delete_specific_user(username):
    Users.query.filter_by(username=username).delete()
    db.session.commit()
    return redirect('/statistics')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = str(request.form.get('username'))
        password = str(request.form.get('password'))
        avail = Users.query.filter_by(username=username).first()
        if not avail:
            user = Users(username = username,
                         password = password,
                         permission=99
                         )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(
            username=username).first()
        if user:
            if user.password == password:
                login_user(user)
                session['username'] = username
                session['permission'] = user.permission
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
@login_required
def index():
    return render_template('index.html')


@app.route('/query_book', methods=['POST'])
@login_required
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
@login_required
def personal_page():
    result = get_all_users()
    return render_template('statistics.html', results=result)


@app.route('/reset/<user_id>', methods=["GET", "POST"])
@login_required
def reset(user_id):
    user = Users.query.filter_by(id=user_id).first()
    return render_template('reset.html', result=user)


@app.route('/update/<user_id>', methods=["POST"])
def update(user_id):
    user = Users.query.filter_by(id=user_id).first()
    user.username = request.form.get('username')
    user.password = request.form.get('password')
    user.permission = int(request.form.get('permission'))
    db.session.commit()
    return redirect('/statistics')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.round((np.divide(val, total) * 100), 2)
    return percent


def data_creation(data, percent, class_labels, group=None):
    for index, item in enumerate(percent):
        data_instance = {}
        data_instance['category'] = class_labels[index]
        data_instance['value'] = item
        data_instance['group'] = group
        data.append(data_instance)


@app.route('/get_all_section_name', methods=['get'])
def get_all_section_name():
    query = db.session.query(Data.section_name, Data.section_id)\
        .distinct(Data.section_name, Data.section_id)\
        .order_by(Data.section_name)
    data = []
    if query:
        for i in query:
            data.append({'section_name': i.section_name,
                         'section_id': i.section_id})
    return jsonify(data)


@app.route('/get_linechart_data')
def get_linechart_data():
    cri = {'section_id': 'ZVCGQ40'}
    hour_labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                   '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
    q = Data.query.filter_by(**cri).filter(Data.time.like('2024/04/20%')).order_by('time')
    data = []
    if q:
        for i in q:
            data.append({
                'time': i.time,
                'section_id': i.section_id,
                'section_name': i.section_name,
                'avg_speed': i.avg_speed,
                'avg_occ': i.avg_occ,
                'total_vol': i.total_vol
            })
    return jsonify(data)


@app.route('/get_piechart_data')
def get_piechart_data():
    contract_labels = ['Month-to-month', 'One year', 'Two year']
    _ = churn_df.groupby('Contract').size().values
    class_percent = calculate_percentage(_, np.sum(_)) #Getting the value counts and total

    piechart_data= []
    data_creation(piechart_data, class_percent, contract_labels)
    return jsonify(piechart_data)


@app.route('/get_barchart_data')
def get_barchart_data():
    tenure_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
    churn_df['tenure_group'] = pd.cut(churn_df.tenure, range(0, 81, 10), labels=tenure_labels)
    select_df = churn_df[['tenure_group','Contract']]
    contract_month = select_df[select_df['Contract']=='Month-to-month']
    contract_one = select_df[select_df['Contract']=='One year']
    contract_two =  select_df[select_df['Contract']=='Two year']
    _ = contract_month.groupby('tenure_group').size().values
    mon_percent = calculate_percentage(_, np.sum(_))
    _ = contract_one.groupby('tenure_group').size().values
    one_percent = calculate_percentage(_, np.sum(_))
    _ = contract_two.groupby('tenure_group').size().values
    two_percent = calculate_percentage(_, np.sum(_))
    _ = select_df.groupby('tenure_group').size().values
    all_percent = calculate_percentage(_, np.sum(_))

    barchart_data = []
    data_creation(barchart_data,all_percent, tenure_labels, "All")
    data_creation(barchart_data,mon_percent, tenure_labels, "Month-to-month")
    data_creation(barchart_data,one_percent, tenure_labels, "One year")
    data_creation(barchart_data,two_percent, tenure_labels, "Two year")
    return jsonify(barchart_data)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
