# selenium
from asyncio.windows_events import NULL
from glob import glob
from importlib.metadata import files
from itertools import count
from re import I
from turtle import goto
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from pandas.core.frame import DataFrame
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlencode, quote_plus
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib

import urllib
import json
import time
import pandas as pd
import requests
import sys

import os
import pickle
import pprint

import datetime
import numpy as np

from tkinter import *
from tkinter import messagebox

from PIL import Image

lastReplyContent = "nothing"

#arg1 = sys.argv[1]
#arg2 = sys.argv[2]
#arg3 = sys.argv[3]
#arg4 = sys.argv[4]

username = ""
password = ""
login_url = "https://www.moneybar.com.tw/login"
url = "https://www.moneybar.com.tw/blogs/moneyvip/31"
searchName = "0128"

_options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
_options.add_experimental_option('prefs', prefs)
_options.add_argument("disable-infobars")
_options.use_chromium = True
_options.add_argument("--start-maximized")  # 最大化視窗
# _options.add_argument("--incognito")  # 開啟無痕模式
_options.add_argument("--disable-popup-blocking ")  # 禁用彈出攔截
# _options.add_argument('--headless')  # 規避google bug
_options.add_argument('--disable-gpu')

# ------ 透過Browser Driver 開啟 Chrome ------
driver = webdriver.Chrome(options=_options)

# 放置 FB 個人發文的基本資訊
listPost = []


class Cookies_operation:
    def getCookies(self):
        # get cookies and save to file"""
        # get login cookies
        driver.maximize_window()
        driver.get('https://www.moneybar.com.tw/login')  # 用來登錄的url
        if True:
            print("plase login in moneybar")
            # 下面為登錄步驟
            # driver.find_element_by_xpath('//div[@id="u1"]/a[@name="tj_login"]').click()
            # time.sleep(2)
            # driver.find_element_by_id("TANGRAM__PSP_10__footerULoginBtn").click()
            #WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID, 'email')))
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="form-inputer"]/input[@name="email"]')))
            driver.find_element(By.XPATH, '//*[@id="form-inputer"]/input[@name="email"]').send_keys(username)
            #WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.ID,'pass')))
            elem = driver.find_element(By.XPATH, '//*[@id="form-inputer"]/input[@name="password"]').send_keys(password)
            elem = driver.find_element(By.XPATH, '//*[@id="member-form-portlet"]/form/button').send_keys(Keys.RETURN)
            # driver.find_element_by_xpath('//button[text()="登錄"]').click()
            # time.sleep(6)
            WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located((By.XPATH, '//*[text()="your account name"]')))
            # if login in successfully,url jump to
            # while driver.current_url == url:
            Cookies = driver.get_cookies()
            pprint.pprint(Cookies)

            outputPath = open('sgCookies.pickle', 'wb')  # 新建一个文件
            pickle.dump(Cookies, outputPath)
            outputPath.close()
            return Cookies


    def readCookies(self):
        # if have cookies file,use it
        # if not,getCSDNCkooies()
        if os.path.exists('sgCookies.pickle'):
            readPath = open('sgCookies.pickle', 'rb')
            Cookies = pickle.load(readPath)
            # print(Cookies)
        else:
            Cookies = Cookies_operation().getCookies()
        return Cookies


def login():
    # ------ 登入的帳號與密碼 ------
    # ------ 前往該網址 ------
    cookies = Cookies_operation().readCookies()
    print(cookies)
    driver.get("https://www.moneybar.com.tw/blogs/moneyvip/31/")
    driver.delete_all_cookies()
    driver.maximize_window()
    for cookie in cookies:
        driver.add_cookie(cookie)
        print(cookie)
    driver.get('https://www.moneybar.com.tw/blogs/moneyvip/31/')


def telegram_bot_sendtext(bot_message):

    bot_token = ''
    bot_chatID = ''
    #bot_groupchatID = '-'
    #bot_groupchatID2 = '-'

    method = 'sendMessage'
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(bot_token, method),
        data={'chat_id': bot_chatID, 'text': bot_message}
    ).json()

    #response2 = requests.post(
    #    url='https://api.telegram.org/bot{0}/{1}'.format(bot_token, method),
    #    data={'chat_id': bot_groupchatID, 'text': bot_message}
    #).json()

    #response3 = requests.post(
    #    url='https://api.telegram.org/bot{0}/{1}'.format(bot_token, method),
    #    data={'chat_id': bot_groupchatID2, 'text': bot_message}
    #).json()

    # response = requests.get(send_text)

    return response





def telegram_bot_sendPhoto(photoAddress):

    bot_token = ''
    bot_chatID = ''
    bot_groupchatID = ''
    #bot_groupchatID2 = ''

    method = 'sendPhoto'

    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}?chat_id={2}'.format(
            bot_token, method, bot_chatID),
        files={'photo': open(photoAddress, 'rb')},
        timeout=60
    )

    response = requests.post(
        url='https://api.telegram.org/bot{0}/{1}?chat_id={2}'.format(
            bot_token, method, bot_groupchatID),
        files={'photo': open(photoAddress, 'rb')}
    )

    #response = requests.post(
    #    url='https://api.telegram.org/bot{0}/{1}?chat_id={2}'.format(
    #        bot_token, method, bot_groupchatID2),
    #    files={'photo': open(photoAddress, 'rb')}
    #)

    # response = requests.get(send_text)
    return response



def backToTop():
    js = "var action=document.documentElement.scrollTop=0"
    driver.execute_script(js)

def lone_capture():
    try:
        WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located((By.XPATH, '//*[text()="葉翼豪"]')))
    except:
        Cookies = Cookies_operation().getCookies()
        print(Cookies)
        driver.get("https://www.moneybar.com.tw/blogs/moneyvip/31/")
    now = "葉芳("+(datetime.datetime.now()).strftime('%Y%m%d')+")"
    found = 0
    while(found==0):
        try:
            today_element = driver.find_element(By.XPATH, "//*[contains(text(),'"+now+"')]")
        except:
            time.sleep(10)
            driver.refresh()
            continue
        else:
            found=1
            today_element.click()
    time.sleep(15)
    window_height = driver.get_window_size()['height']  # 窗口高度
    page_height = driver.execute_script('return document.documentElement.scrollHeight')  # 页面高度
    driver.save_screenshot('qq.png')

    if page_height > window_height:
        n = page_height // window_height  # 需要滚动的次数
        base_mat = np.atleast_2d(Image.open('qq.png'))  # 打开截图并转为二维矩阵

        for i in range(n):
            driver.execute_script(f'document.documentElement.scrollTop={window_height*(i+1)};')
            time.sleep(.5)
            driver.save_screenshot(f'qq_{i}.png')  # 保存截图
            mat = np.atleast_2d(Image.open(f'qq_{i}.png'))  # 打开截图并转为二维矩阵
            base_mat = np.append(base_mat, mat, axis=0)  # 拼接图片的二维矩阵
        Image.fromarray(base_mat).save('hao123.png')
        #im = Image.open('hao123.png')
        #out = im.resize((1920,4000),Image.ANTIALIAS) #resize image with high-quality
        #out.save('hao123.png')
    receivers1 = ['yourmail1@abc.com','yourmail2@abc.com']
    receivers2 = ['abc@gmail.com']
    receivers3 = ['123@hotmail.com']
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "機器人日報"+(datetime.datetime.now()).strftime('%Y%m%d')  #郵件標題
    content["from"] = "abc@gmail.com"  #寄件者
    content["to"] = ', '.join([r for r in receivers1]) #收件者
    #content['Cc'] = "r@hotmail.com"
    content.attach(MIMEImage(Path("hao123.png").read_bytes()))

    def send_mail(_content):
        with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
            try:
                smtp.ehlo()  # 驗證SMTP伺服器
                smtp.starttls()  # 建立加密傳輸
                smtp.login("abc@gmail.com", "abcs14515145")  # 登入寄件者gmail
                smtp.send_message(_content)  # 寄送郵件
                print("Complete!")
            except Exception as e:
                print("Error message: ", e)
    send_mail(content)
    #send_mail(content3)
    
    #all_file_name = os.listdir()
    #for i in all_file_name:
    #    if i.find("qq")>=0:
    #        telegram_bot_sendPhoto(i)
    #        time.sleep(3)
login()
lone_capture()
driver.quit()
