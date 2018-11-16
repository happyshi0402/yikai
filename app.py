#!/usr/bin/env python
# encoding: utf-8
"""
# @Software: PyCharm
# @Author : 王世锋
# @Email：785707939@qq.com
# @Time：2018/11/16 16:43
# @File : app.py
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request, redirect, url_for, jsonify
import flask_login

app = Flask(__name__, static_folder="/home/zkhc_wsf/zkhc_webhook/static")
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = 'hhhhh(Sj1*!@()!$@^*('  # Change this!
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'785707939@qq.com': {'password': 'ly.123456'}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return redirect(url_for('tomcat_log'))
    return 'Bad login'


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


@app.route('/index/')
@flask_login.login_required
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1581)
