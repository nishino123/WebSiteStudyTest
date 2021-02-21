# -*- coding: UTF-8 -*-
# @Time : 2020/7/12 @Author : SUNLIN

"""

    ***************已完成更新**************************
"""

import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
import pymssql
import re
import hashlib


conn = pymssql.connect(server='192.168.101.97',
                           user='sa', password='bjlp@ssw0rd', database='SOP')
cursor = conn.cursor()

sql_update = 'select * from T_BASE_Country_ProductInfo where IsChina = 0 and type = 2'
try:
    # 执行查询语句
    cursor.execute(sql_update)
    # 取得所有结果
    results_hospital = cursor.fetchone()
    Code_Previous = results_hospital[2].encode('latin1').decode('gbk') #之前数据库的第一条数据

except Exception as e:
    print(e)


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


    browser = webdriver.Chrome('chromedriver.exe',chrome_options=option)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
              get: () => undefined
            })
          """
    })  # selenium的反爬虫策略
    for i in range(1000):
        try:
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
                    if (Code_Previous !=item[0].replace('"', "")):
                        print('Code_Previous: ',Code_Previous,'item[0]: ',item[0])
                        parse2json(item, url_Detail)
                    else:
                        exit()  # 当爬出之前的数据时退出更新
        except Exception as e:
            print(e)

    # all_detal_json.append(ylqx)
    browser.close()




def parse2json(content,url_1):
    """
    # type 表示证件类型 1-注册 2-备案
    # IsChina 是否国产 1是国产 0是进口

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

    #共9662条条
    a=content[15]
    b=content[14]




    sql_insert = "" \
                 "if not exists (select top 1 * from T_BASE_Country_ProductInfo where Code  = '%s' and IsChina = 0 and type = 2 )" \
                 " begin " \
                 "INSERT INTO T_BASE_Country_ProductInfo(MD5, Code, RegistrantName, RegistrantAddress, FactoryAddress, ProxyName, ProxyAddress, " \
                 "ProductName, Spec, Describes, UsageDescription, " \
                 "Remark, ApprovalDepartment, ApprovedDate, StorageMethod , Changes,Type, IsChina) " \
                 "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                 "  end " % \
        (content[0].replace('"', ""),url_md5, content[0].replace('"', ""), content[1].replace('"', ""), content[2].replace('"', ""),
         content[3].replace('"', "").replace("\'s", ""), content[4].replace('"', "").replace("\'s", "").replace("\'", ""),
         content[5].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[6].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[7].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[8].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[9].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""),content[10].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
         content[11].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[12].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", ""),
        content[13].replace('"', "").replace("\'s", "").replace("\'", "").replace("\n", "").replace("\r", ""), content[14].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
               , 2, 0)
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
