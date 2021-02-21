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
    conn = pymssql.connect(server='192.168.101.97',
                           user='sa', password='bjlp@ssw0rd', database='SOP')
    cursor = conn.cursor()

    option = None
    if True:
        option = webdriver.ChromeOptions()  # 构造模拟浏览器
        option.add_argument(argument='headless')  # 设置无界面，可选,使用无头模式会验证失败

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
            print('start')
            url_List='http://code.nhsa.gov.cn:8000/ylfw/stdMedicalService/getPublicStdMedicalServiceSubTreeData.html?_search=false&nd=1608536008168&rows=10000&page={}&sidx=t.ms_code&sord=asc&msId=0&msCode=&msName='.format(
                i)
            browser.get(url_List)  # 访问界面
            print('访问界面')
            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            res = json.loads(soup.text)
            length=res['records']
            rows=res['rows']
            for row in rows:
                msId=row['msId']
                msPid=row['msPid']
                msCode=row['msCode']
                msName=row['msName']
                containsContent=row['containsContent']
                excludedContent=row['excludedContent']
                chargeUnit=row['chargeUnit']
                explain=row['explain']

                sql_insert = "INSERT INTO T_BASE_Country_ManufacturerInfo( msId, msPid, msCode, msName, containsContent, " \
                             "excludedContent, chargeUnit, explain) " \
                             "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % \
                             (msId, msPid, msCode, msName, containsContent,excludedContent, chargeUnit, explain
                              )

                print(sql_insert)

        except Exception as e:
            print(e)

    # all_detal_json.append(ylqx)
    browser.close()

    # continue


def parse2json(content):
    """
    类型（1-许可证/2-备案凭证）
    """

    conn = pymssql.connect(server='192.168.101.97',
                           user='sa', password='bjlp@ssw0rd', database='SOP')
    cursor = conn.cursor()




    sql_insert = "INSERT INTO T_BASE_Country_ManufacturerInfo( Code, CompanyName, LegalPerson, CEO, HomeAddress, " \
                 "ProductAddress, ScopeDetail, ApprovalDepartment, ApprovedDate,  " \
                 "ProductionRegistrationForm,Type) " \
                 "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                 ( content[0].replace('"', ""), content[1].replace('"', ""), content[2].replace('"', ""),
                  content[3].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""),
                  content[4].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""),
                  content[5].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""),
                  content[6].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r",
                                                                                                              ""),
                  content[7].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""),
                  content[8].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r",
                                                                                                              ""),
                  content[9].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""),
                  2
                  )

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
