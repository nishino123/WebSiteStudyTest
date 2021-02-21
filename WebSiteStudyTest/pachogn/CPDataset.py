import urllib.parse as p
import time
from selenium import webdriver
import json
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
def get_data_b(browser,tableId,bcId,page,tableName,viewtitleName,viewsubTitleName,title):
    url = "http://app1.nmpa.gov.cn/datasearchcnda/face3/search.jsp?tableId={0}&State=1&bcId={1}&State=1&curstart={2}&State=1&tableName={3}&State=1&viewtitleName={4}&State=1&viewsubTitleName={5}&State=1&tableView={6}&State=1&cid=0&State=1&ytableId=0&State=1&searchType=search&State=1".format(
        tableId,bcId,page,tableName,viewtitleName,viewsubTitleName,p.quote(title))
    try:
        browser.get(url)
        print(page)
    except:
        print("超时")
    time.sleep(2)
    return browser


def getDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    #options.add_argument("--no-sandbox") # linux only
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """
    })
    return driver




def main_browser(tableId,bcId,start_num,end_num,tableName,viewtitleName,viewsubTitleName,title):
    # browser = webdriver.Firefox()
    # options = webdriver.ChromeOptions()
    # browser = webdriver.Chrome(options=options)
    # browser.maximize_window()
    # url = "http://www.nmpa.gov.cn/"
    # browser.get(url)

    profile_directory = r'C:\Users\wangjinhai\AppData\Roaming\Mozilla\Firefox\Profiles\snel70gq.default - release'

    profile = webdriver.FirefoxProfile(profile_directory)
    # 启动浏览器配置
    # driver = webdriver.Firefox(profile)

    browser = webdriver.Firefox(profile)
    url = "http://www.nmpa.gov.cn/"
    browser.get(url)
    time.sleep(5)
    action = ActionChains(browser)
    click_name = browser.find_element_by_link_text('药品')
    action.move_to_element(click_name)

    time.sleep(2)
    click_name.click()
    time.sleep(5)
    click_name = browser.find_element_by_link_text(title)
    click_name.click()
    time.sleep(2)
    for page in range(start_num, end_num):
        browser = get_data_b(browser, tableId, bcId, page, tableName, viewtitleName, viewsubTitleName, title)
        with open("{}{}.txt".format(title, page), 'w+', encoding="utf-8") as f:
            f.write(browser.page_source)
        with open("page.txt", 'w+', encoding='utf-8') as f:
            f.write(str([page + 1, end_num]))


    # options = webdriver.ChromeOptions()
    # options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone"})
    # driver = Chrome(options=options)
    # driver.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
    # driver.get('http://www.nmpa.gov.cn/')
    # driver.get('http://www.baidu.com')

    # driver = getDriver()
    # driver.maximize_window()
    # driver.get('http://app1.nmpa.gov.cn/')
    # # browser.maximize_window()
    #
    # time.sleep(2)
    # # action = ActionChains(browser)
    # # click_name = browser.find_element_by_link_text('医疗器械')
    # # action.move_to_element(click_name)
    # driver.find_element_by_css_selector('a[title="国产一、二、三类注册器械信息"]').click()
    #
    # # browser = driver.find_element_by_link_text('医疗器械')
    #
    # # time.sleep(2)
    # # browser.click()
    # time.sleep(5)
    # click_name = driver.find_element_by_link_text(title)
    # click_name.click()
    # time.sleep(2)
    # for page in range(start_num, end_num):
    #     driver = get_data_b(driver,tableId,bcId,page,tableName,viewtitleName,viewsubTitleName,title)
    #     with open("{}{}.txt".format(title,page),'w+',encoding="utf-8") as f:
    #         f.write(driver.page_source)
    #     with open("page.txt", 'w+',encoding='utf-8') as f:
    #             f.write(str([page+1,end_num]))

start_num = 1
end_num = 11002
tableId = 25
bcId = "152904713761213296322795806604"
tableName = "TABLE25"
viewtitleName = "COLUMN167"
viewsubTitleName="COLUMN821,COLUMN170,COLUMN166"
title = "国产器械"
main_browser(tableId, bcId, start_num, end_num, tableName, viewtitleName, viewsubTitleName, title)
