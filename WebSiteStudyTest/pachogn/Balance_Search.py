# 图鉴平台，查询余额
import json
import requests


def query_balance(uname, pwd):
    param = {"username": uname, "password": pwd}
    result = json.loads(requests.get("http://api.ttshitu.com/queryAccountInfo.json", params=param).text)
    print('图鉴返回的结果：', result)
    print('------------------------------------\n')
    if result['success']:
        return result["data"]
    else:
        return result["message"]
    return ""


if __name__ == "__main__":
    result = query_balance(uname='YONGHUMING', pwd='NOGIZAKA46q')
    balance = result['balance']
    consumed = result['consumed']
    successNum = result['successNum']
    failNum = result['failNum']
    ownNum = int(float(balance) / 0.002)

    print(f'账户余额：{balance}')
    print(f'消费金额：{consumed}')
    print(f'图像识别成功次数：{successNum}')
    print(f'图像识别失败次数：{failNum}')
    print(f'剩余可使用次数：{ownNum}')