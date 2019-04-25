#!/usr/bin/env python
# encoding: utf-8
"""
# @Author : 王世锋
# @Email : 785707939@qq.com
# @Time : 2019/4/19 14:31
# @File : api_test.py
"""
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import requests

url = "http://api.wsf.com:802/api/basis/patientLogin"
head = {'X-Nginx-Proxy': u'true', 'Content-Length': u'121', 'Accept-Encoding': u'gzip', 'X-Forwarded-For': u'192.168.0.112', 'Charset': u'UTF-8', 'Host': 'localhost:802', 'Accept': u'*/*', 'User-Agent': u'Mozilla/5.0 (Linux; Android 5.1; GN8001 Build/LMY47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/47.0.2526.100 Mobile Safari/537.36', 'Connection': u'close', 'Uniquecredence': u'18361157898', 'X-Real-Ip': u'192.168.0.112', 'Sign': u'7840e2556a75fcad91c892616adf608f', 'Content-Type': u'application/x-www-form-urlencoded'}
data = {'osType': [u'android'], 'phoneImei': [u'94:92:bc:18:03:50'], 'account': [u'18361157898'], 'password': [u'jia123'], 'phoneName': [u'GiONEE,OS Version5.1']}
r = requests.request("POST", url, headers=head, data=data)

print r.status_code
print r.text


