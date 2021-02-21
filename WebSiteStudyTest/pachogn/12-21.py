import time
from selenium import webdriver
import pymssql
from bs4 import BeautifulSoup
import json
conn = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor = conn.cursor()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)
for i in range(1000):
    try:
        url_List = 'http://code.nhsa.gov.cn:8000/hc/stdPublishData/getStdPublicDataList.html?releaseVersion=20201024&specificationCode=&commonname=&companyName=&catalogname1=&catalogname2=&catalogname3=&_search=false&nd=1608601896286&rows=1000&page={}&sidx=&sord=asc'.format(
            i)
        driver.get(url_List)  # 访问界面

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        res = json.loads(soup.text)['rows']
        for result in res:
            releaseVersion=result['releaseVersion']
            specificationCode=result['specificationCode']
            catalogname1=result['catalogname1']
            catalogname2=result['catalogname2']
            catalogname3=result['catalogname3']
            commonname=result['commonname']
            matrial=result['matrial']
            characteristic=result['characteristic']
            companyName=result['companyName']

            try:
                url2='http://code.nhsa.gov.cn:8000/hc/stdPublishData/toPublicDetailDialog1.html?specificationCode='+str(specificationCode)+'&releaseVersion='+str(releaseVersion)
                print(url2)
                driver.get(url2
                    )
                boolean = True
                # driver.find_element_by_css_selector('#treeDemo1_1_a').click()
                # 第一个tr是空的

                for i in range(1, 6):
                    # print('i', i)
                    tds_3 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(3)')
                    tds_4 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(4)')
                    tds_5 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(5)')
                    tds_6 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(6)')
                    # print('length: ',len(tds_3))
                    length = len(tds_3) #第一个td_3是空的

                    for j in range(1, length):
                        # print('j: ', j)
                        RegistratioNo=tds_3[j].text
                        Person=tds_4[j].text
                        ProName=tds_5[j].text
                        SpecsNum=tds_6[j].text

                        sql = "INSERT INTO T_BASE_MAMedicareCategory(CodeId, FCategory, SCategory, TCategory, Name, Material, Specs,Company, RegistratioNo, Person, ProName, SpecsNum) " \
                              "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                                  specificationCode,catalogname1,catalogname2,catalogname3,commonname,matrial, characteristic,companyName,
                                  RegistratioNo, Person, ProName, SpecsNum)
                        print(sql)
                    #     # try:
                    #     #     cursor.execute(sql)  # 执行
                    #     #     conn.commit()  # 提交
                    #     # except Exception as msg:
                    #     #     conn.rollback()  # 发生错误时回滚
                    #     #     cursor.execute(sql)
                    #     #     conn.commit()

                time.sleep(2)

            except Exception as e:
                driver.close()
                print(e)
                raise

    except Exception as e:
        print(e)
