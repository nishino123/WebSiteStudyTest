import time
from selenium import webdriver
import pymssql
from bs4 import BeautifulSoup
import json



# conn = pymssql.connect(server='192.168.101.94',
#             user='sa', password='lanp@ssw0rd', database='SOP')

conn = pymssql.connect(server='192.168.101.97',
                       user='sa', password='bjlp@ssw0rd', database='SOP')

cursor = conn.cursor()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)
for i in range(1,1000):
    try:
        url_List = 'http://code.nhsa.gov.cn:8000/hc/stdSpecification/getStdSpecificationListData.html?_search=false&nd=1608694688784&rows=1000&page={}&sidx=specification_code&sord=asc'.format(
            i)
        driver.get(url_List)  # 访问界面

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        res = json.loads(soup.text)['rows']
        for result in res:
            specificationCode=result['specificationCode']
            catalogcode=result['catalogcode']
            catalogname1=result['catalogname1'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            catalogname2=result['catalogname2'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            catalogname3=result['catalogname3'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            commonnamecode=result['commonnamecode'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            commonname=result['commonname'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            matrial=result['matrial'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            matrialcode = result['matrialcode'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            characteristiccode = result['characteristiccode'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            characteristic = result['characteristic'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")

            sql = "" \
                  "if not exists (select top 1 * from T_BASE_MAMedicareBusinessCategory  where Code='%s') " \
                  "  begin  " \
                  "INSERT INTO T_BASE_MAMedicareBusinessCategory(Code, CatalogcodeCode, SubjectOrCategory, UsageOrItem, PartsOrFunctionsOrVarieties, NameCode,Name, Material, MaterialCode, SpecificationCode, Specification ) " \
                  "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                  "  end    " % (
                specificationCode,specificationCode, catalogcode, catalogname1, catalogname2, catalogname3, commonnamecode, commonname, matrial, matrialcode, characteristiccode, characteristic)
            print(sql)

            try:
                cursor.execute(sql)  # 执行
                conn.commit()  # 提交
            except Exception as msg:
                conn.rollback()  # 发生错误时回滚
                cursor.execute(sql)
                conn.commit()

    except Exception as e:
        print(e)
