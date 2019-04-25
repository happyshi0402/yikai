#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2019/4/23 14:44
# @File : m_test.py
"""
import sys


from utils import mysql_tool


host, user, db_name, password, port = "172.16.110.238", "zkhc_root_admin", "zkhc_server_admin", "wasLY,.18zkhc", 548
db = mysql_tool.my_mysql(host, user, db_name, password, port)

sql = "select * from team_info;"
data = db.my_fetchall(sql)
print(data)

