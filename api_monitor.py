#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2019/4/19 13:44
# @File : api_monitor.py
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify
import flask_login, requests
from werkzeug.datastructures import FileStorage

app = Flask(__name__, static_folder="/home/zkhc_wsf/zkhc_webhook/static")
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = 'lyzkhcsdfklj91283jKSJISUA(Sj1*!@()!$@^*('  # Change this!

from utils import mysql_tool


host, user, db_name, password, port = "172.16.110.238", "zkhc_root_admin", "zkhc_server_admin", "wasLY,.18zkhc", 548
db = mysql_tool.my_mysql(host, user, db_name, password, port)

@app.errorhandler(404)
def handlers_404(error):
    """
    404
    :return:
    """
    print("404")
    return "内容不存在,请检查Url后重试！"


@app.before_request
def before_request():
    print("request.headers : ",request.headers)
    print("request.json : ",request.json)
    print("request.args : ",request.args)
    print("request.data : ",request.data)
    print("request.form : ", request.form)
    print("request.files : ", request.files)
    print("request.method, request.url : ",request.method, request.url)
    print("request.url_root : ",request.url_root)
    print("request.url_rule : ",request.url_rule)
    print("request.base_url : ",request.base_url)

    def dict_con(con):
        if con is None:
            con = {}
        else:
            con = dict(con)
        return con

    heades = dict(request.headers)
    host = "http://api.wsf.com/"
    if heades["X-Forwarded-For"] == "192.168.0.102":
        host = "http://api.real.com/"

    data = request.form
    if data == "":
        data = request.data

    base_url = request.base_url
    print(base_url)

    url = str(request.url).replace(request.url_root, host)
    print(url)

    heades["Host"] = "api.wsf.com"
    print(heades)
    data = dict(data)
    print(type(data), data)
    files = request.files
    print("files", files)
    new_files = {}
    if files is not None:
        for file in files:
            file_item = files[file]
            new_files[file] = file_item

    print("new_files", new_files)



    s = requests.request(request.method, url, data = data, headers = heades,
                         params = request.args, json= request.json, files = new_files
                         )


    data = dict_con(data)
    headers = dict_con(request.headers)
    json_data = dict_con(request.json)
    params = dict_con(request.args)
    files = dict_con(request.files)

    host = "http://api.wsf.com"
    method, url = request.method, url.replace(host, "")
    if url[:3] == "pat":
        api_cate = "patient"
        host = 'http://localhost:802'
    else:
        api_cate = "doctor"
        host = 'http://localhost:805'

    sql = "select path from gateway_api_define where path=%s;"
    data = db.my_fetchone(sql, (url))
    if data == []:
        sql = "insert into gateway_api_define (path, api_cate, retryable, strip_prefix, url, enabled)" \
              " VALUES (%s, %s, %s, %s, %s, %s);"
        db.execute(sql, (url, api_cate, 0, 1, host, 1))

    status = "ok"
    version = "1.0.1"
    sql = "insert into " \
          "zkhc_api_history (url, method, data, api_cate, headers, " \
          "json, params, files, status, version, return_data) " \
          "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    import json
    return_data = s.text
    if return_data == "INTERNAL_SERVER_ERROR":
        return_data = str(json.dumps({"status": 500, "message": return_data}))

    db.execute(sql, (url, method, str(json.dumps(data)), api_cate, json.dumps(headers),
                     str(json.dumps(json_data)),
                     str(json.dumps(params)),
                     str(json.dumps(files)),  status, version, return_data))
    print(s.text)
    return s.text, s.status_code



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3700, debug=False, threaded=True)
