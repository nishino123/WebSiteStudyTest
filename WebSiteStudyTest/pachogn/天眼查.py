import requests

url = 'https://en.artprecium.com/catalogue/vente_309_more-than-unique-multiples-estampes/resultat'

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "PHPSESSID=m2hbrvp548cg6v4ssp0l35kcj7; _ga=GA1.2.2052701472.1532920469; _gid=GA1.2.1351314954.1532920469; __atuvc=3%7C31; __atuvs=5b5e9a0418f6420c001",
    "Host": "en.artprecium.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
}
# 构造form表单
data = {"IdEpoque": "",
        "MotCle": "",
        "Order": "",
        "LotParPage": "All",
        "IdTypologie": ""}

response = requests.post(url=url, data=data, headers=headers, timeout=10)

print(response)   # 返回值：<Response [200]>
