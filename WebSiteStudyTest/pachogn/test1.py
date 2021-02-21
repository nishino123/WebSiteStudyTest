# -*- coding: UTF-8 -*-
# @Time : 2020/7/12 @Author : SUNLIN


import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
import pymssql
import re
import hashlib



def main():
    option = None
    if True:
        option = webdriver.ChromeOptions()  # 构造模拟浏览器
        option.add_argument(argument='headless')  # 设置无界面，可选,使用无头模式会验证失败
        option.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})  # 模拟iPhone X浏览

    # try:
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=option)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })  # selenium的反爬虫策略

    for i in range(1,1000):
        try:

            url_List = 'http://mobile.nmpa.gov.cn/datasearch/QueryList?tableId={}&searchF=Quick%20SearchK&pageIndex=1&pageSize=15'.format(
                i)
            url_List = 'http://mobile.nmpa.gov.cn/datasearch/QueryList?tableId='+str(i)+'&searchF=Quick%20SearchK&pageIndex=1&pageSize=15'
            print('第： ',i,'条记录')
            print(url_List)
            browser.get(url_List)  # 访问界面

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            res = json.loads(soup.text)
            print('res: ',res)
            Id = i
            content=res[0]['CONTENT']
            print('Id: ',Id,'CONTENT: ',content)
            parse2json(Id, content)

            # all_detal_json.append(ylqx)

        except Exception as e:  # 不报错，继续运行
            print(e)
            time.sleep(5)
            pass
        continue
    browser.close()

def parse2json(Id, content):
    """
    注册证编号zczbh-----0
    注册人名称zcrmc----1
    注册人住所zcrzs-----2
    生产地址scdz---------3
    产品名称cpmc--------------4
    管理类别gllb--------------5
    型号规格xhgg------------6
    结构及其组成jgjqzc-----------7
    适用范围syfw-----------------8
    批准日期pzrq---------------14
    有效期至yxqz------------------15
    # 注zhu
    生产地址,产品存储条件有效期，附件，其他内容，备注，审批部门，变更情况等均为空，故不作记录

    ....
    :return:json
    """

    conn = pymssql.connect(server='192.168.101.94',
                           user='sa', password='lanp@ssw0rd', database='SOP')
    cursor = conn.cursor()



    sql_insert = "INSERT INTO T_Temp(Id,Content) " \
                 "VALUES ('%s','%s')" % \
                 (Id,content)
    print(sql_insert)

    # cursor.execute(sql_insert)
    # print(sql_insert)
    # conn.commit()

    try:
        cursor.execute(sql_insert)
        conn.commit()
    except Exception as e:
        print('存入数据库失败', e)
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()
