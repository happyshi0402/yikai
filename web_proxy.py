#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2019/4/22 10:15
# @File : web_proxy.py
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')
from flask import Flask, render_template, request, redirect, url_for, jsonify
import flask_login

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = 'lyzkhcsdfklj91283jKSJISUA(Sj1*!@()!$@^*('  # Change this!
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

users = {'785707939@qq.com': {'password': 'kjwsf.0653'}}


class User(flask_login.UserMixin):
    pass

@app.route('/index/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
