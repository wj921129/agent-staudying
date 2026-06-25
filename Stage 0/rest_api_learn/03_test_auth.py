import requests
from utils import section, show_json

def check_httpbin(resp):
    """httpbin 服务不可用时友好提示"""
    if not resp.ok:
        print(f"  ⚠ httpbin.org 暂时不可用（{resp.status_code}），跳过展示。")
        return False
    return True

HTTPBIN = "https://httpbin.org"

headers = {
    "custom-header": "hello-python",
}

response = requests.post(HTTPBIN, headers=headers)
show_json(response)

if check_httpbin(response):
    response_data = response.json()
    print(type(response_data))

