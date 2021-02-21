import time
from selenium import webdriver
import pymssql
from bs4 import BeautifulSoup
import json
import hashlib

def getStrAsMD5(parmStr):
    if isinstance(parmStr, str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()

conn = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor = conn.cursor()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)
for i in range(400):  #还未完成
    try:
        print('i: ',i)
        # if(i!=1):
        #     time.sleep(600)    #数量太多导致爬虫终止,或者从数据库中的记录判断有几条

        url_List = 'http://code.nhsa.gov.cn:8000/hc/stdPublishData/getStdPublicDataList.html?releaseVersion=20201024&specificationCode=&commonname=&companyName=&catalogname1=&catalogname2=&catalogname3=&_search=false&nd=1608601896286&rows=100&page={}&sidx=&sord=asc'.format(
            i)
        driver.get(url_List)  # 访问界面

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        res = json.loads(soup.text)['rows']
        for result in res:
            releaseVersion=result['releaseVersion']
            specificationCode=result['specificationCode']
            catalogname1=result['catalogname1'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            catalogname2=result['catalogname2'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            catalogname3=result['catalogname3'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            commonname=result['commonname'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            matrial=result['matrial'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            characteristic=result['characteristic'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            companyName=result['companyName'].replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            CodeWithoutFactory=specificationCode[:-5]



            sql1 = "" \
                   "if not exists (select top 1 * from T_BASE_MAMedicareCategory  where Code='%s')  " \
                   "   begin  " \
                       "INSERT INTO T_BASE_MAMedicareCategory(Code, CodeWithoutFactory,SubjectOrCategory, UsageOrItem, PartsOrFunctionsOrVarieties, Name, Material, Specification,Factory) " \
                       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                   "   end   " % (
                      specificationCode,specificationCode,CodeWithoutFactory, catalogname1, catalogname2, catalogname3, commonname, matrial, characteristic,
                      companyName)
            print(sql1)

            try:
                cursor.execute(sql1)  # 执行
                conn.commit()  # 提交
            except Exception as msg:
                conn.rollback()  # 发生错误时回滚
                cursor.execute(sql1)
                conn.commit()



            # try:
            #     url2='http://code.nhsa.gov.cn:8000/hc/stdPublishData/toPublicDetailDialog1.html?specificationCode='+str(specificationCode)+'&releaseVersion='+str(releaseVersion)
            #     print(url2)
            #     mdf5=getStrAsMD5(url2)
            #     driver.get(url2
            #         )
            #     boolean = True
            #     # driver.find_element_by_css_selector('#treeDemo1_1_a').click()
            #     # 前几个tr是空的
            #
            #     while boolean:
            #         tds_3 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(3)')
            #         tds_4 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(4)')
            #         tds_5 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(5)')
            #         tds_6 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(6)')
            #         length = len(tds_3)
            #
            #         if(length>1):
            #             boolean=False
            #             for td_k in range(1, length):
            #
            #                 RegistratioNo=tds_3[td_k].text
            #                 Person=tds_4[td_k].text.replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            #                 ProName=tds_5[td_k].text.replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            #                 SpecsNum=tds_6[td_k].text.replace('"', "").replace("\'s", "").replace("\'", "").replace("\\n", "").replace("\\r", "")
            #
            #                 sql = "INSERT INTO T_BASE_MAMedicareCategoryRegistration(MD5,CodeId,RegistratioNo, Person, Name, SpecsNum) " \
            #                       "VALUES ('%s','%s','%s','%s','%s','%s')" % (
            #                           mdf5,specificationCode,RegistratioNo, Person, ProName, SpecsNum)
            #                 print(sql)#数据库中Name的长度小了点,sql语句查询的同时不能执行插入
            #
            #
            #                 try:
            #                     cursor.execute(sql)  # 执行
            #                     conn.commit()  # 提交
            #                 except Exception as msg:
            #                     conn.rollback()  # 发生错误时回滚
            #                     cursor.execute(sql)
            #                     conn.commit()
            #
            #     time.sleep(2)
            #
            # except Exception as e:
            #     driver.close()
            #     print(e)
            #     raise

    except Exception as e:
        print(e)
