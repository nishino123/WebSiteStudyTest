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

conn = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor = conn.cursor()

sql_hospital = ' select *  from T_BASE_MAMedicareHealthOrg' \
               # 'where Region=\'四川\' and Hospital=\'绵阳市中心医院\''     #爬数据的过程中还是会停的
try:
    # 执行查询语句
    cursor.execute(sql_hospital)
    # 取得所有结果
    results_hospital = cursor.fetchall()
    # 打印数据表个数
    # print(len(results_hospital))
    # 打印数据表名，数据表类型，及存储引擎类型
    for row in results_hospital:
        Id=row[0]
        LegalPerson=row[10].encode('latin1').decode('gbk').replace('?','')
        ChargePerson=row[11].encode('latin1').decode('gbk').replace('?','')
        RegistrationNo = row[7].encode('latin1').decode('gbk').replace('?', '')
        Specialty = row[9].encode('latin1').decode('gbk').replace('?', '')
        sql = "update T_BASE_MAMedicareHealthOrg set RegistrationNo='%s', Specialty = '%s', LegalPerson = '%s', ChargePerson = '%s' where Id= '%s'"\
              %(RegistrationNo,Specialty,LegalPerson,ChargePerson,Id)
        print('sql: ', sql)

        try:
            cursor.execute(sql)  # 执行
            conn.commit()  # 提交
        except Exception as msg:
            conn.rollback()  # 发生错误时回滚
            cursor.execute(sql)
            conn.commit()

except Exception as e:
    print(e)
