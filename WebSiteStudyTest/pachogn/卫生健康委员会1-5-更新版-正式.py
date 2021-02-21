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

conn4 = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor4 = conn4.cursor()

conn = pymssql.connect(server='192.168.101.97',
                           user='sa', password='bjlp@ssw0rd', database='SOP')
cursor = conn.cursor()



def getStrAsMD5(parmStr):
    if isinstance(parmStr, str):
        parmStr = parmStr.encode("utf-8")
    m = hashlib.md5()
    m.update(parmStr)
    return m.hexdigest()

def indetify(img_path):
    # print('__RequestVerificationToken: ',__RequestVerificationToken)
    # 获取验证码并识别
    response = session.get(code_url, headers=headers)
    # print(response.content)

    with open(img_path, 'wb') as fp:
        fp.write(response.content)
    # base64_data = base64.b64encode(response.content)
    # b64 = base64_data.decode()
    #
    # data = base64.b64decode(response.content)
    # print('data: ',data)
    # return data


def base64_api(uname, pwd,  img):
    with open(img, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


def download_image_code(img_src, img_name):
    '''下载图片验证码到本地'''
    img_content = requests.get(img_src, headers=headers).content
    with open(img_name, 'wb') as fp:
        fp.write(img_content)
    print(f'验证码图片{img_name}下载成功')

if __name__ == "__main__":
    Id = 27648
    print('start')
    ####################查询具体的机构名称######################################
    hospital_items = {}
    hospital_items_list = []

    # 如果停了，重新运行程序，并更改ID，不要去人为更改

    sql_hospital = ' select *  from Temp_Hospital ' \
                   'where Id >= %s'%(Id) \
        # 'where Region=\'青海\' and Hospital=\'青海省妇幼保健院\''     #爬数据的过程中还是会停的
    try:
        # 执行查询语句
        cursor4.execute(sql_hospital)
        # 取得所有结果
        results_hospital = cursor4.fetchall()
        # 打印数据表个数
        # print(len(results_hospital))
        # 打印数据表名，数据表类型，及存储引擎类型
        time_stop = 1
        for row in results_hospital:
            time_stop = time_stop + 1

            # if(time_stop%300==0):
            #     time.sleep(6000) #暂停100分钟

            Code = row[1]
            Region = row[2].encode('latin1').decode('gbk')
            Hospital = row[3].encode('latin1').decode('gbk')
            hospital_item = {'Code': Code,
                             'Region': Region,
                             'Hospital': Hospital
                             }

            print('Id: ', row[0], hospital_items)

            url = "http://zgcx.nhc.gov.cn:9090/unit/index"
            code_url = "http://zgcx.nhc.gov.cn:9090/CaptchaGenerate/Generate/"
            headers = {
                "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, "
                              "like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36"}
            headers['User-Agent'] = random.choice(USER_AGENT_LIST)
            session = requests.Session()
            response = session.get(url, headers=headers)
            html = etree.HTML(response.content.decode())
            __RequestVerificationToken = html.xpath("//input[@name='__RequestVerificationToken']/@value")[0]

            img_path = 'images/1.png'
            # print('cookies: ',session.cookies)
            indetify(img_path)
            result = base64_api(uname='YONGHUMING', pwd='NOGIZAKA46q', img=img_path)
            # print(result)

            data = {'__RequestVerificationToken': __RequestVerificationToken,
                    'Prov': hospital_item['Code'],
                    'Check_Code': result,
                    'Unit_Name': hospital_item['Hospital']}

            print(data)
            response = requests.post(url, headers=headers, data=data, cookies=session.cookies)
            html = etree.HTML(response.text)  # 将html转换成_Element对象
            items = []
            cls = ""

            trs = html.xpath("//table[contains(@class,'table-bordered')]//tbody/tr")

            for tr in trs:
                tds = tr.xpath("./td")

                # item_dict = {'province': tr.xpath("./td/text()")[0],
                #              'examing_approving_org': tr.xpath("./td/text()")[1],
                #              'hospital': tr.xpath("./td/text()")[2],
                #              'level': tr.xpath("./td/text()")[3],
                #              'href': tr.xpath("./td/a")[0].attrib['href']}

                item_dict = {'province': tds[0].text,
                             'examing_approving_org': tds[1].text,
                             'hospital': tds[2].text,
                             'level': tds[3].text,
                             'href': tr.xpath("./td/a")[0].attrib['href']}

                code = item_dict['href'].split('/')[-1]

                items.append(item_dict)
                detail_URL = 'http://zgcx.nhc.gov.cn:9090' + item_dict['href']
                mdf5 = getStrAsMD5(detail_URL)
                detail_response = requests.get(detail_URL, headers=headers)
                html = etree.HTML(detail_response.text)
                rows = html.xpath("//div[contains(@class,'row')]")
                rows_test = html.xpath("//div[contains(@class,'col-sm-8 col-md-9 field_cxt')]")[4].text
                rows_test_b = html.xpath("//div[contains(@class,'col-sm-8 col-md-9 field_cxt')]")[4].xpath('//b')

                print('rows_test_b',rows_test_b)
                if (rows_test_b):
                    for row_b in rows_test_b:
                        rows_test = rows_test + row_b.text + row_b.tail
                specialty = rows_test

                detail_items = []
                for row in rows:
                    detail_item = row.xpath('./div')[1].text
                    # detail_item = row.xpath('./div/text()')[1]
                    detail_items.append(detail_item)
                effictiveTime = rows[len(rows) - 1].xpath('./div/span/text()')[0]
                disableTime = rows[len(rows) - 1].xpath('./div/span/text()')[2]
                detail_item_dict = {
                    'province': detail_items[0],
                    'examing_approving_org': detail_items[1],
                    'registrationNo': detail_items[2].replace('?', '').replace(' ', '').replace('"', "").replace("\'s",
                                                                                                                 "").replace(
                        "\'", "").replace("\n", "").replace("\r", ""),
                    'adress': detail_items[3],
                    'specialty': specialty.replace('?', '').replace(' ', '').replace('"', "").replace("\'s",
                                                                                                      "").replace("\'",
                                                                                                                  "").replace(
                        "\n", "").replace("\r", ""),
                    'level': detail_items[5],
                    'legalPerson': detail_items[6].replace('?', '').replace(' ', '').replace('"', "").replace("\'s",
                                                                                                              "").replace(
                        "\'", "").replace("\n", "").replace("\r", ""),
                    'chargePerson': detail_items[7].replace('?', '').replace(' ', '').replace('"', "").replace("\'s",
                                                                                                               "").replace(
                        "\'", "").replace("\n", "").replace("\r", ""),
                    'effictiveTime': effictiveTime,
                    'disableTime': disableTime
                }

                # sql1 = "INSERT INTO T_BASE_MAMedicareHealthOrg(Code,Province, ExamingApprovingOrg, HospitalName,  HospitalLevel ) " \
                #        "VALUES ('%s','%s','%s','%s','%s')" % (code,
                #                                               item_dict['province'], item_dict['examing_approving_org'],
                #                                               item_dict['hospital'], item_dict['level'])
                # print('sql1: ', sql1)

                # sql = "" \
                #       "" \
                #       "if not exists (select top 1 * from T_BASE_MAMedicareHealthOrg  where code='%s')  " \
                #    "   begin  " \
                #       "INSERT INTO T_BASE_MAMedicareHealthOrg(MD5,Code,Province, ExaminingApprovingOrg, HospitalName,  HospitalLevel, RegistrationNo, Address,Specialty,LegalPerson,ChargePerson,EffectiveTime,DisableTime) " \
                #       "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                #     "   end    " % (
                #     code,mdf5, code,
                #                                                                                      item_dict[
                #                                                                                          'province'],
                #                                                                                      item_dict[
                #                                                                                          'examing_approving_org'],
                #                                                                                      item_dict[
                #                                                                                          'hospital'],
                #                                                                                      item_dict[
                #                                                                                          'level'],
                #                                                                                      detail_item_dict[
                #                                                                                          'registrationNo'],
                #                                                                                      detail_item_dict[
                #                                                                                          'adress'],
                #                                                                                      detail_item_dict[
                #                                                                                          'specialty'],
                #                                                                                      detail_item_dict[
                #                                                                                          'legalPerson'],
                #                                                                                      detail_item_dict[
                #                                                                                          'chargePerson'],
                #                                                                                      detail_item_dict[
                #                                                                                          'effictiveTime'],
                #                                                                                      detail_item_dict[
                #                                                                                          'disableTime']
                #                                                                                      )

                sql = "INSERT INTO T_BASE_MAMedicareHealthOrg(MD5,Code,Province, ExaminingApprovingOrg, HospitalName,  HospitalLevel, RegistrationNo, Address,Specialty,LegalPerson,ChargePerson,EffectiveTime,DisableTime) " \
                      "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (mdf5, code,
                                                                                                     item_dict[
                                                                                                         'province'],
                                                                                                     item_dict[
                                                                                                         'examing_approving_org'],
                                                                                                     item_dict[
                                                                                                         'hospital'],
                                                                                                     item_dict[
                                                                                                         'level'],
                                                                                                     detail_item_dict[
                                                                                                         'registrationNo'],
                                                                                                     detail_item_dict[
                                                                                                         'adress'],
                                                                                                     detail_item_dict[
                                                                                                         'specialty'],
                                                                                                     detail_item_dict[
                                                                                                         'legalPerson'],
                                                                                                     detail_item_dict[
                                                                                                         'chargePerson'],
                                                                                                     detail_item_dict[
                                                                                                         'effictiveTime'],
                                                                                                     detail_item_dict[
                                                                                                         'disableTime']
                                                                                                     )
                print('sql: ', sql)
                try:
                    cursor.execute(sql)  # 执行
                    conn.commit()  # 提交
                    time.sleep(1) #休息一下

                except Exception as msg:
                    conn.rollback()  # 发生错误时回滚
                    cursor.execute(sql)
                    conn.commit()

                print('detail_item_dict: ', detail_item_dict)
                print('detail_URL: ', detail_URL)
            print(items)


    except Exception as e:
        raise e





