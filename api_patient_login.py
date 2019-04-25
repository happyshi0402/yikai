#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2019/4/19 15:04
# @File : api_patient_login.py
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import requests

url = "http://192.168.0.5:802/api/basis/patientLogin"


payload = "account=18361157898&password=jia123&undefined="
headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Postman-Token': "fe8d6170-d002-42d0-a62f-6b4c4cafe939"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)