#!/usr/local/bin/python2.7
# encoding=utf8
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header
from os.path import getsize
from sys import exit
from re import compile, IGNORECASE
import sys, time
import os

# 定义主机 帐号 密码 收件人 邮件主题

# 定义主机 帐号 密码 收件人 邮件主题
mail_info = {
    "from": "ihelp@ai-kang.cn",
    "to": "wangshifengly@dingtalk.com",
    "hostname": "smtp.ym.163.com",
    "username": "ihelp@ai-kang.cn",
    "password": "Lyzkhc0606",
    "mail_subject": "zkhc 服务器异常",
    "mail_text": "hello, tomcat服务器出现异常了!,请及时处理",
    "mail_encoding": "utf-8"
}


# 发送邮件函数
def send_mail(error):
    # 定义邮件的头部信息
    # 连接SMTP服务器，然后发送信息
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])
    msg = MIMEText(error, "plain", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]
    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
    smtp.quit()


def isRunning(process_name):
    try:
        process = len(os.popen('docker ps | grep "' + process_name + '" | grep -v grep').readlines())
        if process >= 1:
            return True
        else:
            return False
    except:
        print("Check process ERROR!!!")
        return False


def isPsRunning(process_name):
    try:
        process = len(os.popen('ps -aux| grep "' + process_name + '" | grep -v grep').readlines())
        if process >= 1:
            return True
        else:
            return False
    except:
        print("Check process ERROR!!!")
        return False

# 调用发送邮件函数发送邮件
if __name__ == '__main__':
    process_name = "zkhc_tomcat_dev"
    isrunning = isRunning(process_name)
    import os
    print(isrunning)
    if isrunning == False:
        send_mail("老铁!zkhc tomcat dev 服务器挂了!")
        os.system("docker restart zkhc_tomcat_dev_545")
        send_mail("老铁!zkhc tomcat dev docker 环境已经重启了!")

    # process_name = "znkf_508"
    # isrunning = isPsRunning(process_name)
    # print(isrunning)
    # if isrunning == False:
    #     send_mail("老铁!zkhc 后台系统508 dev 环境挂了!")
    #     os.system("sh /home/zkhc_wsf/start_admin_dev.sh 508 dev 542")
    #     send_mail("老铁!zkhc 后台系统508 dev 环境已经重启了!")