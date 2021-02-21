# -*- coding: UTF-8 -*-
# @Time : 2020/7/12 @Author : SUNLIN


import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
import pymssql
import re
import hashlib

def getStrAsMD5(parmStr):

    if isinstance(parmStr,str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()

def main():
    option = None
    if True:
        option = webdriver.ChromeOptions()  # 构造模拟浏览器
        option.add_argument(argument='headless')  # 设置无界面，可选,使用无头模式会验证失败
        option.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})  # 模拟iPhone X浏览

    try:
        browser = webdriver.Chrome('chromedriver.exe',chrome_options=option)
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
        })  # selenium的反爬虫策略
        for i in range(1, 1000):
            url_List = 'http://mobile.nmpa.gov.cn/datasearch/QueryList?tableId=104&searchF=Quick%20SearchK&pageIndex={}&pageSize=1000'.format(i)


            browser.get(url_List)  # 访问界面

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            res = json.loads(soup.text)
            for result in res:
                Id = result['ID']
                url_Detail = 'http://mobile.nmpa.gov.cn/datasearch/QueryRecord?tableId=104&searchF=ID&searchK=%s' % Id
                print('url_Detail: ',url_Detail)
                browser.get(url_Detail)
                response = browser.page_source
                html = BeautifulSoup(response, 'html.parser')
                ylqx = html.body.get_text()
                # ylqx.replace('\t', '')

                print('第'+str(i)+'条数据： ',ylqx) #因为有的数据取到的是空，所以才会出现list index out of range,所以不用去管它
                # print('type: ', type(ylqx))
                # print('正则表达式提取特定字符串： ',re.findall(r"^CONTENT\w",ylqx))
                ylqx=ylqx[1:-1]

                # print('正则表达式： ',re.findall(r"CONTENT.*?\}",ylqx))
                ylqx=re.findall(r"CONTENT.*?\}",ylqx)
                # print(ylqx[17][9:-1])
                item=[]
                for k in range(len(ylqx)):
                    item.append(ylqx[k][9:-1])
                if len(item) == 0:
                    pass
                else:
                    parse2json(item, url_Detail)

        # all_detal_json.append(ylqx)
        browser.close()
    except Exception as e: #不报错，继续运行
        print(e)
        time.sleep(5)
        pass
    # continue



def parse2json(content,url_1):
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

    url_md5 = getStrAsMD5(url_1)

    #判断是否字节的长度是否过长，数据库最大也只能存储8000个字节，4000个汉字
    # print(len(content[6]))
    # print(len(content[7]))
    # print(len(content[8]))
    # if (len(content[7])>4000):
    #     content[7]=content[7][:4000]
    # print(len(content[7]))

    # sql_insert = "insert into T_BASE_Country_ProductInfo values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
    #     (content[0], content[1], content[2], content[3], content[4], content[5],
    #     content[6], content[7], content[8], content[9], content[10], content[11],
    #     content[12], content[13], content[14], content[15], content[16],
    #     content[17])
    # type 表示证件类型 1-注册 2-备案
    # IsChina 是否国产 1是国产 0是进口
    a=content[15]
    b=content[14]
    # sql_insert = "INSERT INTO T_BASE_Country_ProductInfo(MD5, Code, RegistrantName, RegistrantAddress, FactoryAddress, ProductName, [Level], Spec, MainComponent, UsageDescription, StorageMethod, " \
    #              "ExtralFile, ExtralInfo, Remark, ApprovalDepartment, ApprovedDate, Validuntil, Changes, Type, IsChina) " \
    #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
    #     (url_md5, content[0].replace('"', ""), content[1].replace('"', ""), content[2].replace('"', ""),
    #      content[3].replace('"', "").replace("\'s", ""), content[4].replace('"', "").replace("\'s", "").replace("\'", ""),
    #      content[5].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[6].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
    #      content[7].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[8].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
    #      content[9].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[10].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
    #      content[11].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[12].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
    #     content[13].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[14].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
    #      content[15].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[16].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
    #      , 2, 0)
    # print(url_1)

    sql_insert = "INSERT INTO T_BASE_Country_ProductInfo(MD5, Code, RegistrantName, RegistrantAddress, FactoryAddress, ProductName, [Level], Spec, MainComponent, UsageDescription, StorageMethod, " \
                 "ExtralFile, ExtralInfo, Remark, ApprovalDepartment, ApprovedDate, Validuntil, Changes, Type, IsChina) " \
          "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
        (url_md5, content[0].replace('"', ""), content[1].replace('"', ""), content[2].replace('"', ""),
         content[3].replace('"', "").replace("\'s", ""), content[4].replace('"', "").replace("\'s", "").replace("\'", ""),
         content[5].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[6].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[7].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[8].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[9].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[10].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[11].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[12].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
        content[13].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[14].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[15].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[16].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
         , 2, 0)
    print(url_1)

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
