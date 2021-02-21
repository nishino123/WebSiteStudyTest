import requests
from lxml import etree
from setting import USER_AGENT_LIST
import random
import base64
import json
import requests
import hashlib
import pymssql
import time
import json

conn = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor = conn.cursor()



def getStrAsMD5(parmStr):
    if isinstance(parmStr, str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()



if __name__ == "__main__":
    url = 'https://api.dayi.org.cn:9997/api/institution/list?pageSize=20'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'upgrade-insecure-requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        # 'cookie': 'xxx;yyy;zzz',
        # 'referer': 'https://xxx.yyy.zzz'
    }

    # 发起get请求
    response = requests.get(url, headers=headers, verify=True)
    # 获取html文本
    html_data = response.content.decode()
    main_data=json.loads(html_data)
    data_list=main_data['list']
    for hospital_data in data_list:
        id = hospital_data['id']
        name = hospital_data['name']
        address=hospital_data['address']
        telephone = hospital_data['telephone']
        thumbnail = hospital_data['thumbnail']
        level = hospital_data['level']
        insurance = hospital_data['insurance']
        special = hospital_data['special'].replace('<p>','').replace('</p','').replace('<n>','').replace('</n>','').replace('>','')
        intro = hospital_data['intro'].replace('<p>','').replace('</p','').replace('<n>','').replace('</n>','')

        sql = " insert into medicalInformationHospital(id,name,address,telephone,thumbnail,level,insurance,special,intro)" \
              " values('%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(id,name,address,telephone,thumbnail,level,insurance,special,intro)
        print(sql)


