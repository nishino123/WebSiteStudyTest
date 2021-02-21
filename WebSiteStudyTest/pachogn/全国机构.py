import requests
from lxml import etree
from setting import USER_AGENT_LIST,PROVINCE_CODE_MAP
import random
import base64
import json
import requests
import hashlib
import pymssql

conn = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor = conn.cursor()

headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, "
                              "like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
headers['User-Agent']=random.choice(USER_AGENT_LIST)

region_URL='https://m.haodf.com/touch/province/list.htm'
region_response=requests.get(region_URL,headers=headers)
# print(region_response.text)  #html
tree=etree.HTML(region_response.text)
#/tobody/tbody/tobody/tr[3]
# table_element = tree.xpath("/html/body/div[4]/table")[0]

table_element = tree.xpath("//a[contains(@href,'https://m.haodf.com/touch/hospital/')] ")


for row in table_element:
    try:
        hosptial_url=row.attrib['href']
        region = row.text
        code=PROVINCE_CODE_MAP[region]

        hosptial_response = requests.get(hosptial_url, headers=headers)
        hospital_tree = etree.HTML(hosptial_response.text)
        uls_element = hospital_tree.xpath("//div[@class='mt15 ml10 mr10 bg_w b_ra5 mb50']/ul")
        for ul in uls_element:
            hospital_lis = ul.xpath('li')
            for hospital_li in hospital_lis:
                hospital=hospital_li.xpath('div/p')[0].text.replace(' ','').replace('\n','')
                # s1 = etree.tostring(hospital).decode('utf-8')
                print(code,region,hospital)
                sql1 = "" \
                       "if not exists (select top 1 * from Temp_Hospital  where Hospital='%s')" \
                       "   begin   " \
                       "INSERT INTO Temp_Hospital(Code,region,hospital) " \
                       "VALUES ('%s','%s','%s')" \
                       "" \
                       "   end    " % (hospital,code,region,hospital)
                print('sql1: ', sql1)
                try:
                    cursor.execute(sql1)  # 执行
                    conn.commit()  # 提交
                except Exception as msg:
                    conn.rollback()  # 发生错误时回滚
                    cursor.execute(sql1)
                    conn.commit()


            hospital_li=hospital_lis[0]


    except Exception as error:
        pass


