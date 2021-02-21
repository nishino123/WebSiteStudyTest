
import base64
import json
import requests

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


if __name__ == "__main__":
    img_path = "http://zgcx.nhc.gov.cn:9090/CaptchaGenerate/Generate/"
    result = base64_api(uname='YONGHUMING', pwd='NOGIZAKA46q', img=img_path)
    print(result)