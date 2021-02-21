import time
from selenium import webdriver
import pymssql
conn = pymssql.connect(server='192.168.101.94',
            user='sa', password='lanp@ssw0rd', database='SOP')
cursor = conn.cursor()
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome(options=options)
try:
    driver.maximize_window()
    driver.get('http://code.nhsa.gov.cn:8000/search.html?sysflag=1003')
    driver.switch_to.frame('dataInfo')
    time.sleep(1)
    Datalist = []
    big_obj = {}
    k = 1
    boolean = True
    while boolean:
        tds_second = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(2)')
        tds_third = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(3)')
        tds_forth = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(4)')
        tds_fifth = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(5)')
        tds_sixth = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(6)')
        tds_seventh = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(7)')
        tds_eighth = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(8)')
        tds_nineth = driver.find_elements_by_css_selector('#gridlist>tbody> tr>td:nth-child(9)')
        detaile = driver.find_elements_by_css_selector("#gridlist>tbody> tr>td:nth-child(10)")
        length = len(tds_second)
        for i in range(1, length):
            sql = "INSERT INTO T_BASE_MAMedicareCategory(Code, SubjectOrCategory, UsageOrItem, PartsOrFunctionsOrVarieties, Name, Material, Specification,Factory) " \
                  "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                      Linedata['CodeId'], Linedata['FCategory'], Linedata['SCategory'], Linedata['TCategory'],
                      Linedata['Name'], Linedata['Material'], Linedata['Specs'], Linedata['Company'],
                      detaile1[j].text, detaile2[j].text, detaile3[j].text, detaile4[j].text)


            obj = {
                    'CodeId': tds_second[i].text,
                    'FCategory': tds_third[i].text,
                    'SCategory': tds_forth[i].text,
                    'TCategory': tds_fifth[i].text,
                    'Name': tds_sixth[i].text,
                    'Material': tds_seventh[i].text,
                    'Specs': tds_eighth[i].text,
                    'Company': tds_nineth[i].text
                }
            Datalist.append(obj)

        for i in range(1, length):

            detaile[i].click()
            time.sleep(2)
            driver.switch_to.frame(driver.find_element_by_tag_name("iframe")) # 无name和id情况下寻找Iframe
            time.sleep(1)
            detaile1 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(3)')
            detaile2 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(4)')
            detaile3 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(5)')
            detaile4 = driver.find_elements_by_css_selector('#gridlist2>tbody> tr>td:nth-child(6)')
            Linedata = Datalist[i-1]
            for j in range(1, len(detaile1)):
                sql = "INSERT INTO T_BASE_MAMedicareCategory(CodeId, FCategory, SCategory, TCategory, Name, Material, Specs,Company, RegistratioNo, Person, ProName, SpecsNum) " \
                      "VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
                    Linedata['CodeId'], Linedata['FCategory'], Linedata['SCategory'], Linedata['TCategory'], Linedata['Name'], Linedata['Material'], Linedata['Specs'], Linedata['Company'],
                    detaile1[j].text, detaile2[j].text, detaile3[j].text, detaile4[j].text)
                try:
                    cursor.execute(sql)  # 执行
                    conn.commit()  # 提交
                except Exception as msg:
                    conn.rollback()  # 发生错误时回滚
                    cursor.execute(sql)
                    conn.commit()
            time.sleep(1)
            driver.switch_to.parent_frame()
            driver.find_element_by_css_selector('.ui-dialog tbody>tr>td>.ui-dialog-close').click()
            # if i % 4 == 0:
            print(i)
            if k % 3 == 0:
                driver.execute_script("window.scrollTo(0,%s)" % (i*57.5))
            else:
                driver.execute_script("window.scrollTo(0,%s)" % (i * 59.5))
        time.sleep(1)
        str_class = driver.find_element_by_css_selector('#next_gridpage').get_attribute('class')
        print(str_class, 111111)
        if 'x-item-disabled' not in str_class:
            k = k+1
            time.sleep(1)
            driver.find_element_by_css_selector('#next_gridpage').click()
            time.sleep(2)
            driver.refresh()
            driver.execute_script("window.scrollTo(0,0)")
        else:
            boolean = False
except Exception as e:
    driver.close()
    print(e)
    raise

#     print(driver.find_element_by_css_selector('.content #gridlist>tbody>tr:nth-child(2)>td:nth-child(2)').get_attribute('title'))
#
#     time.sleep(0.5)
#     driver.find_element_by_css_selector('#ext-gen51').get_attribute('value')
#     time.sleep(0.5)
#     driver.find_element_by_css_selector('#ext-gen134 #ext-gen144').click()
#     time.sleep(2)
#     driver.switch_to.frame('subMenu216_IFrame')
#
#     # 选择产品组
#     driver.find_element_by_css_selector('#cbProductLine').click()
#     time.sleep(0.5)
#     product_divs = driver.find_elements_by_css_selector('.x-resizable-pinned>div>div')
#     lengths = len(product_divs)
#     for length in range(lengths):
#         if length==0:
#             product_divs[length].click()
#         else:
#             driver.find_element_by_css_selector('#cbProductLine').click()
#             time.sleep(0.5)
#             product_divs[length].click()
#         # 选择单据状态为待接收
#         driver.find_element_by_css_selector('#cbReceiptStatus').click()
#         time.sleep(0.5)
#         status_divs = driver.find_elements_by_css_selector('.x-layer.x-combo-list >div>div')
#         for i in status_divs:
#             if i.text == '待接收':
#                 i.click()
#         time.sleep(0.5)
#         # 点击查询按钮
#         driver.find_element_by_css_selector('#ext-gen19').click()
#         time.sleep(10)
#         # 获取当前页全部打开明细的按钮
#         buttons = driver.find_elements_by_css_selector('#ext-gen221>div>table>tbody>tr>td:last-child button')
#         for i in buttons:
#             i.click()
#             time.sleep(3.5)
#             WhOutId = driver.find_element_by_css_selector('#DetailWindow #txtPONbr').get_attribute('value')
#             list = []
#             big_obj = {}
#             boolean = True
#             while boolean:
#                 tds_first = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(1)>div')
#                 tds_second = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(2)>div')
#                 tds_third = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(3)>div')
#                 tds_forth = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(4)>div')
#                 tds_fifth = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(5)>div')
#                 tds_sixth = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(6)>div')
#                 tds_seventh = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(7)>div')
#                 tds_eighth = driver.find_elements_by_css_selector('#DetailWindow .x-grid3-body>div tr>td:nth-child(8)>div')
#                 length = len(tds_first)
#
#                 for i in range(1, length):
#                     obj = {
#                         'ItemName': '',
#                         'ItemModel': tds_first[i].text,
#                         'ItemLot': tds_second[i].text,
#                         'DisableDate': tds_third[i].text,
#                         'RcvNum': tds_forth[i].text,
#                         'ApprovalNum': tds_fifth[i].text,
#                         'EffectiveDate': tds_sixth[i].text,
#                         'Type': 1
#                     }
#                     list.append(obj)
#                 # 判断是不是要翻页
#                 str_class = driver.find_element_by_css_selector('#DetailWindow #ext-gen351>table').get_attribute('class')
#                 print(str_class, 111111)
#                 if 'x-item-disabled' not in str_class:
#                     driver.find_element_by_css_selector('#DetailWindow #ext-gen353').click()
#                     time.sleep(5)
#                 else:
#                     boolean = False
#             big_obj = {
#                 'receiptLines': list,
#                 'SupplierName': '上海康健进出口有限公司',
#                 'OrgId': '1001702210000022',
#                 'WhOutId': WhOutId,
#                 'Type': 1
#             }
#
#             print(big_obj)
#             headers = {
#                 'Content-Type': 'application/json;charset=utf-8',
#                 'Authorization': 'Bearer acbce215-f22e-476e-aea0-b697dbac850c'
#             }
#             url = 'http://192.168.200.23:9037/api/CGBRecognition_Info/AddCGBRecognition_Info'
#
#             # data = big_obj
#             data = json.dumps(big_obj)
#             r = requests.post(url, data, headers=headers)
#             print(r.status_code)
#             # 关闭弹框
#             driver.find_element_by_css_selector('#ext-gen265').click()
except Exception as e:
    driver.close()
    print(e)
    raise